from  flask import Flask, request, jsonify
import mysql.connector
import os
import requests

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME")
    )

@app.route("/relacion")
def relacion():
    usuarios = requests.get("http://usuarios:5000/usuarios").json()

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT nombre FROM mascotas")
    mascotas = cursor.fetchall()
    connection.close()
    
    resultado = [
        {"usuario": usuarios[0]["nombre"], "mascota": mascotas[0][0]}
    ]
    return jsonify(resultado)

#---------- Relacion de todos
@app.route("/relaciont")
def relacion_todos():
    usuarios = requests.get("http://usuarios:5000/usuarios").json()

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT nombre FROM mascotas")
    mascotas = cursor.fetchall()
    connection.close()
    
    resultado = [
        {"usuario": u["nombre"], "mascota": m[0]}

        for u, m in zip(usuarios, mascotas)
    ]
    return jsonify(resultado)


#------ Usuario especifico con id desde backend (puerto 5000)
@app.route("/usuario/<int:id>")
def usuario(id):
    usuarios = requests.get(f"http://usuarios:5000/usuarios/{id}").json()
    return jsonify (usuarios)   


@app.route("/")
def home():
    return "API FUNCIONANDO"

@app.route("/mascotas", methods = ["POST"])
def crear_mascota():
    data = request.json
    connection = get_connection
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO mascotas (nombre, tipo) VALUES (%s, %s)",
        (data["nombre"], data["tipo"])
    )
    connection.commit()
    connection.close()
    
@app.route("/mascotas", methods = ["GET"])
def listar_mascotas():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM mascotas")
    mascotas = cursor.fetchall()
    connection.close()
    return jsonify(mascotas)

@app.route("/mascotas/<int:id>", methods = ["GET"])
def listar_mascotas_id(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM mascotas WHERE id = %s", (id,))
    mascota = cursor.fetchone()
    connection.close()
    return jsonify(mascota)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)