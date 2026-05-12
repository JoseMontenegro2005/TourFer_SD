from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

UMBRAL_FALLOS = 3
TIEMPO_ESPERA = 10  # segundos para intentar recuperación


SERVICIOS = {
    "mascotas": {
        "url": "http://backend:5000/mascotas",
        "fallos": 0,
        "estado": "CLOSED",
        "tiempo_apertura": None
    },
    "usuarios": {
        "url": "http://usuarios:5000/usuarios",
        "fallos": 0,
        "estado": "CLOSED",
        "tiempo_apertura": None
    }
}


# CIRCUIT BREAKER


def ejecutar_con_circuit_breaker(nombre_servicio):
    servicio = SERVICIOS[nombre_servicio]
    ahora = time.time()

  
    # ESTADO OPEN

    if servicio["estado"] == "OPEN":
        tiempo_transcurrido = ahora - servicio["tiempo_apertura"]

        if tiempo_transcurrido < TIEMPO_ESPERA:
            restante = int(TIEMPO_ESPERA - tiempo_transcurrido)

            print(f"[CB] {nombre_servicio}: OPEN ({restante}s restantes)", flush=True)

            return {
                "error": f"Servicio '{nombre_servicio}' temporalmente bloqueado",
                "estado": "OPEN",
                "reintento_en": restante
            }, 503

        # Pasar a HALF-OPEN
        servicio["estado"] = "HALF_OPEN"
        print(f"[CB] {nombre_servicio}: pasando a HALF_OPEN", flush=True)


    # INTENTO (CLOSED o HALF_OPEN)
    try:
        response = requests.get(servicio["url"], timeout=2)
        response.raise_for_status()

        if servicio["estado"] == "HALF_OPEN":
            print(f"[CB] {nombre_servicio}: recuperación exitosa → CLOSED", flush=True)
        else:
            print(f"[CB] {nombre_servicio}: OK", flush=True)

        servicio["fallos"] = 0
        servicio["estado"] = "CLOSED"
        servicio["tiempo_apertura"] = None

        return response.json(), 200

    except Exception as e:
        print(f"[CB] {nombre_servicio}: fallo -> {e}", flush=True)

        # Si estaba probando (HALF_OPEN) → vuelve a OPEN
        if servicio["estado"] == "HALF_OPEN":
            servicio["estado"] = "OPEN"
            servicio["tiempo_apertura"] = ahora

            print(f"[CB] {nombre_servicio}: fallo en HALF_OPEN → OPEN", flush=True)

            return {
                "error": f"Servicio '{nombre_servicio}' sigue inestable",
                "estado": "OPEN"
            }, 503

        # Si estaba en CLOSED → contar fallos
        servicio["fallos"] += 1

        if servicio["fallos"] >= UMBRAL_FALLOS:
            servicio["estado"] = "OPEN"
            servicio["tiempo_apertura"] = ahora

            print(f"[CB] {nombre_servicio}: circuito ABIERTO", flush=True)

        return {
            "error": f"Fallo de conexión con el servicio '{nombre_servicio}'",
            "estado": servicio["estado"],
            "fallos": servicio["fallos"]
        }, 500


# ENDPOINTS

@app.route("/mascotas")
def mascotas():
    datos, status = ejecutar_con_circuit_breaker("mascotas")
    return jsonify(datos), status


@app.route("/usuarios")
def usuarios():
    datos, status = ejecutar_con_circuit_breaker("usuarios")
    return jsonify(datos), status


@app.route("/resumen")
def resumen():
    datos_m, status_m = ejecutar_con_circuit_breaker("mascotas")
    datos_u, status_u = ejecutar_con_circuit_breaker("usuarios")

    if status_m != 200 or status_u != 200:
        return jsonify({
            "error": "Uno o más servicios no están disponibles",
            "detalle": {
                "mascotas": datos_m,
                "usuarios": datos_u
            }
        }), 503

    return jsonify({
        "mascotas": datos_m,
        "usuarios": datos_u
    }), 200


@app.route("/estado")
def estado():
    resultado = {}

    for nombre, s in SERVICIOS.items():
        info = {
            "estado": s["estado"],
            "fallos": s["fallos"]
        }

        if s["estado"] == "OPEN" and s["tiempo_apertura"]:
            restante = max(0, TIEMPO_ESPERA - (time.time() - s["tiempo_apertura"]))
            info["reintento_en"] = int(restante)

        resultado[nombre] = info

    return jsonify(resultado)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)