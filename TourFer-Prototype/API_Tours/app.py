from flask import Flask, jsonify, request
from functools import wraps
from config import Config, get_api_key
from db import get_db_connection
import MySQLdb.cursors # <--- CAMBIO: Necesario para recibir diccionarios

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"estado": "activo", "servicio": "Catálogo Tours"}), 200

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == get_api_key():
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Acceso no autorizado"}), 401
    return decorated_function

# --- RUTAS PÚBLICAS ---

@app.route('/tours', methods=['GET'])
def get_all_tours():
    conn = get_db_connection(Config) # Pasamos Config si tu db.py lo requiere
    # CAMBIO: Usamos DictCursor de MySQLdb
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    
    cur.execute("SELECT * FROM tours")
    tours = cur.fetchall()
    
    cur.close()
    conn.close()
    return jsonify(tours)

@app.route('/tours/<int:id>', methods=['GET'])
def get_tour_by_id(id):
    conn = get_db_connection(Config)
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    
    cur.execute("SELECT * FROM tours WHERE id = %s", (id,))
    tour = cur.fetchone()
    
    cur.close()
    conn.close()
    
    if tour:
        return jsonify(tour)
    return jsonify({"error": "Tour no encontrado"}), 404

@app.route('/guias', methods=['GET'])
def get_all_guias():
    conn = get_db_connection(Config)
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    
    cur.execute("SELECT id, nombre, email, biografia FROM guias")
    guias = cur.fetchall()
    
    cur.close()
    conn.close()
    return jsonify(guias)

# --- RUTAS PROTEGIDAS (Escritura) ---

@app.route('/tours', methods=['POST'])
@require_api_key
def create_tour():
    data = request.get_json()
    conn = get_db_connection(Config)
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    
    try:
        # CAMBIO: MySQL no soporta RETURNING id en el INSERT.
        cur.execute(
            """
            INSERT INTO tours (nombre, destino, descripcion, duracion_horas, precio, cupos_disponibles, guia_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (data['nombre'], data['destino'], data['descripcion'], data['duracion_horas'], 
             data['precio'], data['cupos_disponibles'], data.get('guia_id'))
        )
        conn.commit()
        
        # CAMBIO: Obtenemos el ID generado así:
        new_id = cur.lastrowid
        
        cur.close()
        conn.close()
        return jsonify({"mensaje": "Tour creado exitosamente", "id": new_id}), 201
        
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"error": str(e)}), 500

@app.route('/tours/<int:id>', methods=['PUT'])
@require_api_key
def update_tour(id):
    data = request.get_json()
    conn = get_db_connection(Config)
    cur = conn.cursor()
    
    try:
        cur.execute("""
            UPDATE tours
            SET nombre = %s,
                destino = %s,
                descripcion = %s,
                duracion_horas = %s,
                precio = %s,
                cupos_disponibles = %s,
                guia_id = %s
            WHERE id = %s
        """, (data['nombre'], data['destino'], data['descripcion'], data['duracion_horas'], 
              data['precio'], data['cupos_disponibles'], data.get('guia_id'), id))
        
        conn.commit()
        rows_affected = cur.rowcount # Funciona igual en MySQL
        cur.close()
        conn.close()
        
        if rows_affected == 0:
            return jsonify({"error": "Tour no encontrado"}), 404
            
        return jsonify({"mensaje": "Tour actualizado exitosamente"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/tours/<int:id>', methods=['DELETE'])
@require_api_key
def delete_tour(id):
    conn = get_db_connection(Config)
    cur = conn.cursor()
    
    try:
        cur.execute("DELETE FROM tours WHERE id = %s", (id,))
        conn.commit()
        rows_affected = cur.rowcount
        
        cur.close()
        conn.close()

        if rows_affected == 0:
            return jsonify({"error": "Tour no encontrado para eliminar"}), 404

        return jsonify({"mensaje": "Tour eliminado exitosamente"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/tours/<int:id>/cupos', methods=['PATCH'])
@require_api_key
def update_tour_cupos(id):
    data = request.get_json()
    conn = get_db_connection(Config)
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    
    try:
        cur.execute("SELECT cupos_disponibles FROM tours WHERE id = %s", (id,))
        tour = cur.fetchone()

        if not tour:
            cur.close()
            conn.close()
            return jsonify({"error": "Tour no encontrado"}), 404

        cupos_actuales = tour['cupos_disponibles']
        cantidad = data['cantidad']
        accion = data['accion']

        if accion == 'decrementar':
            if cupos_actuales >= cantidad:
                nuevos_cupos = cupos_actuales - cantidad
            else:
                cur.close()
                conn.close()
                return jsonify({"error": "No hay suficientes cupos disponibles"}), 409
        elif accion == 'incrementar':
            nuevos_cupos = cupos_actuales + cantidad
        else:
            cur.close()
            conn.close()
            return jsonify({"error": "Acción no válida"}), 400

        # Ejecutamos el update
        cur.execute("UPDATE tours SET cupos_disponibles = %s WHERE id = %s", (nuevos_cupos, id))
        conn.commit()
        
        cur.close()
        conn.close()
        return jsonify({"mensaje": f"Cupos actualizados. Nuevo total: {nuevos_cupos}"})
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/guias', methods=['POST'])
@require_api_key
def create_guia():
    data = request.get_json()
    conn = get_db_connection(Config)
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    
    try:
        # CAMBIO: Quitamos RETURNING id
        cur.execute(
            "INSERT INTO guias (nombre, email) VALUES (%s, %s)", 
            (data['nombre'], data['email'])
        )
        conn.commit()
        # CAMBIO: Usamos lastrowid
        new_id = cur.lastrowid
        
        cur.close()
        conn.close()
        return jsonify({"mensaje": "Guía creado exitosamente", "id": new_id}), 201
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"error": f"Error al crear guía: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)