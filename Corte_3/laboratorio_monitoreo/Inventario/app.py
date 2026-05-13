from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/inventario")
def obtener_inventario():
    return jsonify([
        {"id_producto": 1, "nombre": "Teclado Mecánico", "stock": 45},
        {"id_producto": 2, "nombre": "Monitor 24 pulgadas", "stock": 12},
        {"id_producto": 3, "nombre": "Mouse Inalámbrico", "stock": 0}
    ])
@app.route("/estado")
def estado():
    return  jsonify([
        {"Status": "OK"}
    ])
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)