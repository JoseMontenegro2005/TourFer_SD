from flask import Flask, jsonify, request
import requests
from config import Config, get_catalogo_api_config
from db import get_db_connection
import MySQLdb
from MySQLdb.cursors import DictCursor
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from functools import wraps
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Configuración de API externa
catalogo_api_config = get_catalogo_api_config()
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
def wake_up_all_services():
    try:
        url_notif = 'https://tourfer-notificaciones.onrender.com/'
        print(f"⏰ [Keep-Alive] Despertando Notificaciones...", flush=True)
        requests.get(url_notif, timeout=3)
    except:
        pass #

    try:
        url_catalogo = 'https://tourfer-catalogo.onrender.com/' 
        
        print(f"⏰ [Keep-Alive] Despertando Catálogo...", flush=True)
        requests.get(url_catalogo, timeout=3)
    except Exception as e:
        print(f"⚠️ [Keep-Alive] No se pudo despertar Catálogo: {e}", flush=True)

threading.Thread(target=wake_up_all_services).start()

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('rol_id') == 1:
            return fn(*args, **kwargs)
        else:
            return jsonify({"error": "Acceso no autorizado: Se requiere rol de administrador"}), 403 
    return wrapper

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nombre = data['nombre']
    email = data['email']
    password = data['password']

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    conn = get_db_connection(Config)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, password_hash)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
    except MySQLdb.IntegrityError:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"error": "El email ya existe"}), 409
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Faltan email o password"}), 400

    conn = get_db_connection(Config)
    cur = conn.cursor(cursorclass=DictCursor)
    cur.execute("SELECT id, nombre, password, rol_id FROM usuarios WHERE email = %s", (email,))
    usuario = cur.fetchone()
    cur.close()
    conn.close()

    if usuario and bcrypt.check_password_hash(usuario['password'], password):
        rol = {"rol_id": usuario['rol_id']}
        
        access_token = create_access_token(
            identity=str(usuario['id']),
            additional_claims=rol
        )
        return jsonify({
            "access_token": access_token,
            "user_name": usuario['nombre'] 
        })
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

@app.route('/admin/usuarios', methods=['GET'])
@admin_required
def get_all_users():
    conn = get_db_connection(Config)
    cur = conn.cursor(cursorclass=DictCursor)
    cur.execute("SELECT id, nombre, email, rol_id FROM usuarios")
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(usuarios)


@app.route('/reservas', methods=['POST'])
@jwt_required() 
def create_reserva():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    tour_id = data['tour_id']
    cantidad_personas = data['cantidad_personas']
    fecha = data.get('fecha', 'Fecha sin definir')
    
    # 1. Validar Tour con API externa
    try:
        tour_url = f"{catalogo_api_config['url']}/tours/{tour_id}"
        response = requests.get(tour_url)
        if response.status_code != 200:
            return jsonify({"error": "El tour solicitado no existe"}), 404
        tour_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al comunicar con API Catálogo: {e}"}), 503

    # 2. Validar cupos
    if tour_data['cupos_disponibles'] < cantidad_personas:
        return jsonify({
            "error": "No hay suficientes cupos disponibles",
            "cupos_disponibles": tour_data['cupos_disponibles']
        }), 409

    costo_total = float(tour_data['precio']) * cantidad_personas
    
    # 3. Insertar en BD
    conn = get_db_connection(Config)
    cur = conn.cursor(cursorclass=DictCursor)
    user_email = "sin_correo@tourfer.com"
    
    try:
        cur.execute(
            """
            INSERT INTO reservas (tour_id, usuario_id, cantidad_personas, costo_total, estado) 
            VALUES (%s, %s, %s, %s, %s) 
            """,
            (tour_id, current_user_id, cantidad_personas, costo_total, 'Confirmada') 
        )
        conn.commit()
        reserva_id = cur.lastrowid

        cur.execute("SELECT email FROM usuarios WHERE id = %s", (current_user_id,))
        usuario_data = cur.fetchone()
        if usuario_data:
            user_email = usuario_data['email']

    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"error": f"Error guardando reserva: {str(e)}"}), 500
    
    cur.close()
    conn.close()

    # 4. Actualizar cupos en API externa
    try:
        update_cupos_url = f"{catalogo_api_config['url']}/tours/{tour_id}/cupos"
        headers = {'X-API-Key': catalogo_api_config['key']}
        payload = {'accion': 'decrementar', 'cantidad': cantidad_personas}
        
        requests.patch(update_cupos_url, json=payload, headers=headers)
    except requests.exceptions.RequestException as e:
        print(f"ADVERTENCIA: Reserva {reserva_id} creada, pero falló la actualización de cupos: {e}")
    
    # 5. Enviar Notificación (Con destino y timeout extendido)
    try:
        notificaciones_url = 'https://tourfer-notificaciones.onrender.com/enviar-correo'
        
        headers = {
            'Content-Type': 'application/json',
            'X-Notification-Key': 'clave_segura_local_123' # Asegúrate que coincida con tu variable de entorno
        }
        
        # Obtenemos el destino del objeto tour_data que ya consultamos arriba
        destino_tour = tour_data.get('destino', 'destino turístico')
        nombre_tour = tour_data.get('nombre', 'Tour')

        mensaje_personalizado = (
            f"¡Hola! La reserva #{reserva_id} para el tour '{nombre_tour}' "
            f"con destino a {destino_tour} para la fecha {fecha} ha sido confirmada.\n\n"
            f"Detalles:\n"
            f"- Personas: {cantidad_personas}\n"
            f"- Total: ${costo_total:,.0f}\n\n"
            f"¡Gracias por elegirnos!\n"
            f"TourFer"
        )

        # Aumentamos el timeout a 15 segundos para evitar errores si el servicio está "dormido"
        requests.post(notificaciones_url, json={
            "email": user_email,
            "mensaje": mensaje_personalizado
        }, headers=headers, timeout=15) 
        
    except Exception as e:
        print(f"ADVERTENCIA: No se pudo enviar la notificación: {e}")

    return jsonify({
        "mensaje": "Reserva creada exitosamente",
        "reserva_id": reserva_id,
        "costo_total": costo_total
    }), 201

    
@app.route('/mis-reservas', methods=['GET'])
@jwt_required()
def get_mis_reservas():
    current_user_id = get_jwt_identity()
    conn = get_db_connection(Config)
    cur = conn.cursor(cursorclass=DictCursor)
    cur.execute("SELECT * FROM reservas WHERE usuario_id = %s", (current_user_id,))
    reservas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(reservas)

# --- RUTAS PROXY ADMIN ---

@app.route('/admin/tours', methods=['POST'])
@admin_required
def admin_create_tour():
    data = request.get_json()
    url = f"{catalogo_api_config['url']}/tours"
    headers = {'X-API-Key': catalogo_api_config['key']}
    try:
        response = requests.post(url, json=data, headers=headers)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al comunicar con API Catálogo: {e}"}), 503

@app.route('/admin/tours/<int:id>', methods=['PUT'])
@admin_required
def admin_update_tour(id):
    data = request.get_json()
    url = f"{catalogo_api_config['url']}/tours/{id}"
    headers = {'X-API-Key': catalogo_api_config['key']}
    try:
        response = requests.put(url, json=data, headers=headers)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al comunicar con API Catálogo: {e}"}), 503

@app.route('/admin/tours/<int:id>', methods=['DELETE'])
@admin_required
def admin_delete_tour(id):
    url = f"{catalogo_api_config['url']}/tours/{id}"
    headers = {'X-API-Key': catalogo_api_config['key']}
    try:
        response = requests.delete(url, headers=headers)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al comunicar con API Catálogo: {e}"}), 503
    
@app.route('/admin/guias', methods=['POST'])
@admin_required
def admin_create_guia():
    data = request.get_json()
    url = f"{catalogo_api_config['url']}/guias"
    headers = {'X-API-Key': catalogo_api_config['key']} 
    try:
        response = requests.post(url, json=data, headers=headers)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al comunicar con API Catálogo: {e}"}), 503

@app.route('/public/tours', methods=['GET'])
def public_get_all_tours():
    url = f"{catalogo_api_config['url']}/tours"
    try:
        response = requests.get(url)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al comunicar con API Catálogo: {e}"}), 503

@app.route('/public/tours/<int:id>', methods=['GET'])
def public_get_tour_by_id(id):
    url = f"{catalogo_api_config['url']}/tours/{id}"
    try:
        response = requests.get(url)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al comunicar con API Catálogo: {e}"}), 503

@app.route('/public/guias', methods=['GET'])
def public_get_all_guias():
    url = f"{catalogo_api_config['url']}/guias"
    try:
        response = requests.get(url)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al comunicar con API Catálogo: {e}"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)