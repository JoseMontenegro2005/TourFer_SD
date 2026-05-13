from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

URL_PEDIDOS = "http://pedidos:5000"
URL_INVENTARIO = "http://inventario:5000"
URL_PAGOS = "http://pagos:5000"

fallos = {
   "pedidos" : 0,
   "inventario": 0,
   "pagos": 0
}

@app.route("/pedidos")
def pedidos():
    try:
        inicio = time.time()
        print("[GATEWAY] Accediendo a pedidos", flush=True)
        respuesta = requests.get(f"{URL_PEDIDOS}/pedidos", timeout=2)
        fin = time.time()
        print(f"[INFO] Tiempo respuesta: {fin-inicio}",flush=True)
        return jsonify(respuesta.json()), respuesta.status_code
    except requests.exceptions.RequestException:
        fallos["pedidos"]+=1
        print(f"[WARNING] Error en API pedidos, total fallos en API: {fallos['pedidos']}", flush=True)
        return jsonify({"error": "Servicio de pedidos no disponible"}), 503
        

@app.route("/inventario")
def inventario():
    try:
        inicio = time.time()
        print("[GATEWAY] Accediendo a inventario", flush=True)
        respuesta = requests.get(f"{URL_INVENTARIO}/inventario", timeout=2)
        fin = time.time()
        print(f"[INFO] Tiempo respuesta: {fin-inicio}",flush=True)
        return jsonify(respuesta.json()), respuesta.status_code
    except requests.exceptions.RequestException:
        fallos["inventario"]+=1
        print(f"[WARNING] Error en API inventario, total fallos en API: {fallos['inventario']}", flush=True)
        return jsonify({"error": "Servicio de inventario no disponible"}), 503

@app.route("/pagos")
def pagos():
    try:
        inicio = time.time()
        print("[GATEWAY] Accediendo a pagos", flush=True)
        respuesta = requests.get(f"{URL_PAGOS}/pagos", timeout=2)
        fin = time.time()
        print(f"[INFO] Tiempo respuesta: {fin-inicio}",flush=True)
        return jsonify(respuesta.json()), respuesta.status_code
    except requests.exceptions.RequestException:
        fallos["pagos"]+=1
        print(f"[WARNING] Error en API pagos, total fallos en API: {fallos['pagos']}", flush=True)
        return jsonify({"error": "Servicio de pagos no disponible"}), 503

@app.route("/resumen")
def resumen():
    try:
        inicio = time.time()
        print("[GATEWAY] Accediendo a pedidos", flush=True)
        res_pedidos = requests.get(f"{URL_PEDIDOS}/pedidos", timeout=2)
        fin = time.time()
        print(f"[INFO] Tiempo respuesta: {fin-inicio}",flush=True)
        res_p = res_pedidos.json()
    except requests.exceptions.RequestException:
        fallos["pedidos"]+=1
        print(f"[WARNING] Error en API pedidos, total fallos en API: {fallos['pedidos']}", flush=True)
        res_p = {"error": "Servicio de pedidos caido"}

    try:
        inicio = time.time()
        print("[GATEWAY] Accediendo a pagos", flush=True)
        res_pagos = requests.get(f"{URL_PAGOS}/pagos", timeout=2)
        fin = time.time()
        print(f"[INFO] Tiempo respuesta: {fin-inicio}",flush=True)
        res_pa = res_pagos.json()
    except requests.exceptions.RequestException:
        fallos["pagos"]+=1
        print(f"[WARNING] Error en API pagos, total fallos en API: {fallos['pagos']}", flush=True)
        res_pa = {"error": "Servicio de pagos caido"}

    try:
        inicio = time.time()
        print("[GATEWAY] Accediendo a inventario", flush=True)
        res_inventario = requests.get(f"{URL_INVENTARIO}/inventario", timeout=2)
        fin = time.time()
        print(f"[INFO] Tiempo respuesta: {fin-inicio}",flush=True)
        res_i = res_inventario.json()
    except requests.exceptions.RequestException:
        fallos["inventario"]+=1
        print(f"[WARNING] Error en API inventario, total fallos en API: {fallos['inventario']}", flush=True)
        res_i = {"error": "Servicio de inventario caido"}

    return jsonify({
        "Pedidos":  res_p,
        "Pagos":  res_pa,
        "Inventario":  res_i
    }), 200


@app.route("/estado")
def estado_general():

    try:
        inicio = time.time()
        print("[GATEWAY] Accediendo a API pedidos", flush=True)
        res_pedidos = requests.get(f"{URL_PEDIDOS}/estado", timeout=2)
        fin = time.time()
        print(f"[INFO] Tiempo respuesta: {fin-inicio}",flush=True)
        estado_p = res_pedidos.json()
    except requests.exceptions.RequestException:
        fallos["pedidos"]+=1
        print(f"[WARNING] Error en API pedidos, total fallos en API: {fallos['pedidos']}", flush=True)
        estado_p = {"error": "Servicio de pedidos caido"}

    try:
        inicio = time.time()
        print("[GATEWAY] Accediendo a API pagos", flush=True)
        res_pagos = requests.get(f"{URL_PAGOS}/estado", timeout=2)
        fin = time.time()
        print(f"[INFO] Tiempo respuesta: {fin-inicio}",flush=True)
        estado_pa = res_pagos.json()
    except requests.exceptions.RequestException:
        fallos["pagos"]+=1
        print(f"[WARNING] Error en API pagos, total fallos en API: {fallos['pagos']}", flush=True)
        estado_pa = {"error": "Servicio de pagos caido"}

    try:
        inicio = time.time()
        print("[GATEWAY] Accediendo a API inventario", flush=True)
        res_inventario = requests.get(f"{URL_INVENTARIO}/estado", timeout=2)
        fin = time.time()
        print(f"[INFO] Tiempo respuesta: {fin-inicio}",flush=True)
        estado_i = res_inventario.json()
    except requests.exceptions.RequestException:
        fallos["inventario"]+=1
        print(f"[WARNING] Error en API inventario, total fallos en API: {fallos['inventario']}", flush=True)
        estado_i = {"error": "Servicio de inventario caido"}

    return jsonify({
        "gateway": "OK",
        "Pedidos":  estado_p,
        "Pagos":  estado_pa,
        "Inventario":  estado_i
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)