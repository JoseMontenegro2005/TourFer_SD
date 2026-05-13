from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/pagos")
def obtener_pagos():
    return jsonify([
        {"id_transaccion": 5001, "id_pedido": 101, "estado_pago": "aprobado"},
        {"id_transaccion": 5002, "id_pedido": 102, "estado_pago": "rechazado"}
    ])

@app.route("/estado")
def estado():
    return jsonify([
        {"Status": "OK"}
    ])
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)