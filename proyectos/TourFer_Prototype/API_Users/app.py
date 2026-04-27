from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from config import Config
from db import get_db_connection

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# --- REGISTRO DE USUARIOS ---
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    # Hasheo de la contraseña
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    conn = get_db_connection(Config)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, pw_hash)
        )
        conn.commit()
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": "El usuario ya existe o hubo un error en la DB"}), 409
    finally:
        cur.close()
        conn.close()

# --- LOGIN (GENERACIÓN DE TOKEN) ---
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection(Config)
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, password, rol_id FROM usuarios WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and bcrypt.check_password_hash(user['password'], password):
        # El rol_id es clave para que Reservas sepa si es Admin o Cliente
        claims = {"rol_id": user['rol_id']}
        access_token = create_access_token(identity=str(user['id']), additional_claims=claims)
        
        return jsonify({
            "access_token": access_token,
            "user_name": user['nombre']
        }), 200
    
    return jsonify({"error": "Credenciales inválidas"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)