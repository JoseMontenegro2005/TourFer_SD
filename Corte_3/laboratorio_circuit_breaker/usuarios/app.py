from  flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/usuarios")
def usuarios():
    return jsonify([
        {"id":1, "nombre": "Dopier"},
        {"id":2, "nombre": "Jose"},
        {"id":3, "nombre": "Felipe"}
    ])


#------ Usuario especifico con id
@app.route("/usuarios/<int:id>")
def obtener_usuario(id):
    datos_usuarios = [
        {"id": 1, "nombre": "Dopier"},
        {"id": 2, "nombre": "Jose"},
        {"id": 3, "nombre": "Felipe"}
    ]
    
    for usuario_id in datos_usuarios:
        if usuario_id["id"] == id:
            return jsonify(usuario_id)
            
    return jsonify({"error": "No encontrado"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
