from flask import Flask, request, jsonify
import mysql.connector
import os
import requests

app = Flask(__name__)


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


@app.route("/relacion")
def relacion():
    try:
        usuarios = requests.get("http://usuarios:5000/usuarios", timeout=2).json()
    except requests.RequestException:
        usuarios = []

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT nombre FROM mascotas")
    mascota = cursor.fetchone()
    cursor.close()
    connection.close()

    nombre_usuario = usuarios[0]["nombre"] if usuarios else "Sin usuario"
    nombre_mascota = mascota["nombre"] if mascota else "Sin mascota"

    return {"usuario": nombre_usuario, "Mascota": nombre_mascota}


@app.route("/")
def home():
    return "API FUNCIONANDO"


@app.route("/mascotas", methods=["POST"])
def crear_mascotas():
    data = request.json
    if not data or "nombre" not in data or "tipo" not in data:
        return {"error": "falta nombre o tipo"}, 400

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO mascotas (nombre, tipo) VALUES (%s, %s)",
        (data["nombre"], data["tipo"]),
    )
    connection.commit()
    cursor.close()
    connection.close()

    return {"mensaje": "mascota creada"}


@app.route("/mascotas", methods=["GET"])
def listar_mascotas():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mascotas")
    mascotas = cursor.fetchall()
    cursor.close()
    connection.close()
    return {"mascotas": mascotas}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)