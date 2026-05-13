from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/pedidos")
def obtener_pedidos():
    return jsonify([
        {"id_pedido": 101, "cliente": "Dopier", "total": 150.50, "estado": "procesando"},
        {"id_pedido": 102, "cliente": "Jose", "total": 89.99, "estado": "enviado"}
    ])

@app.route("/estado")
def estado():
    return jsonify([
        {"Status": "OK"}
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)