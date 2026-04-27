from flask import Flask, jsonify, request
from functools import wraps
from config import Config
from db import get_db_connection
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- DECORADOR DE SEGURIDAD ---
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == Config.CATALOGO_API_KEY:
            return f(*args, **kwargs)
        return jsonify({"error": "Acceso no autorizado: API Key inválida"}), 401
    return decorated_function

# --- RUTAS PÚBLICAS (LECTURA) ---

@app.route('/tours', methods=['GET'])
def get_all_tours():
    conn = get_db_connection(Config)
    cur = conn.cursor()
    cur.execute("SELECT * FROM tours")
    tours = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(tours), 200

@app.route('/tours/<int:id>', methods=['GET'])
def get_tour_by_id(id):
    conn = get_db_connection(Config)
    cur = conn.cursor()
    cur.execute("SELECT * FROM tours WHERE id = %s", (id,))
    tour = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(tour) if tour else (jsonify({"error": "Tour no encontrado"}), 404)

@app.route('/guias', methods=['GET'])
def get_all_guias():
    conn = get_db_connection(Config)
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, email, biografia FROM guias")
    guias = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(guias), 200

# --- RUTAS PROTEGIDAS (ESCRITURA / ADMIN) ---

@app.route('/tours', methods=['POST'])
@require_api_key
def create_tour():
    data = request.get_json()
    conn = get_db_connection(Config)
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO tours (nombre, destino, descripcion, duracion_horas, precio, cupos_disponibles, guia_id) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (data['nombre'], data['destino'], data['descripcion'], data['duracion_horas'], 
             data['precio'], data['cupos_disponibles'], data.get('guia_id'))
        )
        conn.commit()
        return jsonify({"mensaje": "Tour creado", "id": cur.lastrowid}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/tours/<int:id>/cupos', methods=['PATCH'])
@require_api_key
def update_tour_cupos(id):
    data = request.get_json()
    cantidad = data.get('cantidad')
    accion = data.get('accion') # 'incrementar' o 'decrementar'
    
    conn = get_db_connection(Config)
    cur = conn.cursor()
    try:
        cur.execute("SELECT cupos_disponibles FROM tours WHERE id = %s", (id,))
        tour = cur.fetchone()
        if not tour: return jsonify({"error": "No existe"}), 404

        nuevos_cupos = tour['cupos_disponibles'] - cantidad if accion == 'decrementar' else tour['cupos_disponibles'] + cantidad
        
        if nuevos_cupos < 0: return jsonify({"error": "Cupos insuficientes"}), 409

        cur.execute("UPDATE tours SET cupos_disponibles = %s WHERE id = %s", (nuevos_cupos, id))
        conn.commit()
        return jsonify({"mensaje": "Cupos actualizados", "nuevo_total": nuevos_cupos}), 200
    finally:
        cur.close()
        conn.close()

@app.route('/tours/<int:id>', methods=['DELETE'])
@require_api_key
def delete_tour(id):
    conn = get_db_connection(Config)
    cur = conn.cursor()
    cur.execute("DELETE FROM tours WHERE id = %s", (id,))
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Eliminado"}) if affected > 0 else (jsonify({"error": "No encontrado"}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)