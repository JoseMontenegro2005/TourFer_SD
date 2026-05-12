from flask import Flask, jsonify
import requests
from requests.exceptions import RequestException
import time

app = Flask(__name__)

# Configuración del patrón Circuit Breaker
CIRCUIT_THRESHOLD = 3          # Número de fallos antes de abrir el circuito
CIRCUIT_RESET_SECONDS = 15    # Tiempo para rearmar el circuito y probar de nuevo

# AQUÍ NACEN LOS CIRCUITOS (UNO POR SERVICIO EXTERNO)
# Cada microservicio dependiente mantiene su propio estado
service_states = {
    "usuarios": {"failure_count": 0, "status": "closed", "opened_at": None},  # 🔌 Circuito 1
    "backend": {"failure_count": 0, "status": "closed", "opened_at": None},   # 🔌 Circuito 2
}

# Dependencias externas que el gateway protege
# Estas son las llamadas que pueden fallar
service_endpoints = {
    "usuarios": "http://usuarios:5000/usuarios",
    "backend": "http://backend:5000/mascotas",
}


# FUNCIÓN QUE VALIDA EL TIEMPO DE ESPERA Y PASA A HALF-OPEN
def reset_circuit_if_needed(service_name):
    state = service_states[service_name]

    # Si el circuito está abierto y ya pasó el tiempo de espera, paso a HALF-OPEN
    if state["status"] == "open" and state["opened_at"] is not None:
        if time.time() - state["opened_at"] >= CIRCUIT_RESET_SECONDS:
            state["status"] = "half_open"
            print(f"Circuito en HALF-OPEN para {service_name}", flush=True)


#  AQUÍ VIVE LA LÓGICA REAL DEL CIRCUIT BREAKER
def call_service(service_name, timeout=2):
    reset_circuit_if_needed(service_name)
    state = service_states[service_name]

    # SI EL CIRCUITO ESTÁ ABIERTO, NO DEJA HACER LA PETICIÓN
    if state["status"] == "open":
        return {"error": f"Servicio {service_name} temporalmente bloqueado"}, 503

    url = service_endpoints[service_name]
    try:
        # Intento de llamada al microservicio
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()

        # Si responde bien, se reinician los fallos y cerramos el circuito
        state["failure_count"] = 0
        state["status"] = "closed"
        state["opened_at"] = None
        return response.json(), response.status_code

    except RequestException as error:
        state["failure_count"] += 1
        print(f"Fallo en {service_name}: {error}", flush=True)

        # Si está en HALF-OPEN o supera el umbral, abrimos el circuito de nuevo
        if state["status"] == "half_open" or state["failure_count"] >= CIRCUIT_THRESHOLD:
            state["status"] = "open"
            state["opened_at"] = time.time()
            print(f"Circuito abierto para {service_name}", flush=True)

        return {"error": f"Servicio {service_name} no disponible"}, 503


# ================= ENDPOINTS DEL GATEWAY =================

# ESTE ENDPOINT USA EL CIRCUITO DEL SERVICIO "usuarios"
@app.route("/usuarios")
def usuarios():
    payload, status = call_service("usuarios")
    return jsonify(payload), status


#  ESTE ENDPOINT USA EL CIRCUITO DEL SERVICIO "backend" (mascotas)
@app.route("/mascotas")
def mascotas():
    payload, status = call_service("backend")
    return jsonify(payload), status


#  ESTE ENDPOINT NO TIENE CIRCUITO PROPIO
# Es un AGREGADOR que depende de DOS servicios externos
# Por eso USA los dos circuitos existentes
@app.route("/resumen")
def resumen():
    usuarios_payload, usuarios_status = call_service("usuarios")  # 🔌 Usa circuito usuarios
    mascotas_payload, mascotas_status = call_service("backend")   # 🔌 Usa circuito backend

    resumen_result = {
        "usuarios": usuarios_payload,
        "mascotas": mascotas_payload,
    }

    # Si ambos servicios responden bien
    if usuarios_status == 200 and mascotas_status == 200:
        return jsonify(resumen_result), 200

    # Si uno falla, devuelve respuesta parcial (gracias a los circuitos)
    return jsonify(resumen_result), 207


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)