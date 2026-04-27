from flask import Flask, jsonify, request
import requests
from config import Config
from db import get_db_connection
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
jwt = JWTManager(app)

@app.route('/mis-reservas', methods=['GET'])
@jwt_required()
def get_mis_reservas():
    current_user_id = get_jwt_identity()
    conn = get_db_connection(Config)
    cur = conn.cursor()
    cur.execute("SELECT * FROM reservas WHERE usuario_id = %s", (current_user_id,))
    reservas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(reservas), 200

@app.route('/reservas', methods=['POST'])
@jwt_required() 
def create_reserva():
    user_id = get_jwt_identity()
    data = request.get_json()
    tour_id = data.get('tour_id')
    cantidad = data.get('cantidad_personas')

    try:
        headers = {'X-API-Key': Config.CATALOGO_API_KEY}
        payload = {"cantidad": cantidad, "accion": "decrementar"}
        
        patch_resp = requests.patch(
            f"{Config.CATALOGO_API_URL}/tours/{tour_id}/cupos",
            json=payload,
            headers=headers,
            timeout=10 
        )

        if patch_resp.status_code != 200:
            error_msg = patch_resp.json().get('error', 'Error desconocido')
            return jsonify({"error": f"Catálogo rechazó la operación: {error_msg}"}), patch_resp.status_code

        tour_data = patch_resp.json() 

    except requests.exceptions.Timeout:
        return jsonify({"error": "El Catálogo tardó demasiado en responder. Intenta de nuevo."}), 504
    except Exception as e:
        return jsonify({"error": f"No se pudo conectar con el Catálogo: {str(e)}"}), 503

    precio_unidad = data.get('precio_unidad', 0) 
    total = precio_unidad * cantidad

    conn = get_db_connection(Config)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO reservas (tour_id, usuario_id, cantidad_personas, costo_total, estado) VALUES (%s, %s, %s, %s, %s)",
            (tour_id, user_id, cantidad, total, 'Confirmada')
        )
        reserva_id = cur.lastrowid
        conn.commit()

        print(f"[EVENTO]: Reserva {reserva_id} guardada exitosamente.")
        return jsonify({"mensaje": "Reserva creada", "id": reserva_id}), 201

    except Exception as e:
        conn.rollback()
        requests.patch(
            f"{Config.CATALOGO_API_URL}/tours/{tour_id}/cupos",
            json={"cantidad": cantidad, "accion": "incrementar"},
            headers={'X-API-Key': Config.CATALOGO_API_KEY}
        )
        return jsonify({"error": f"Error al guardar reserva, cupos devueltos: {str(e)}"}), 500
    finally:
        cur.close()
        conn.close()
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)