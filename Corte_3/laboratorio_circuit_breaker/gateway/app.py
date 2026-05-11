from flask import Flask, request, jsonify
import requests
import time


app= Flask(__name__)

fallos = {
    "usuarios": 0,
    "mascotas": 0
}

circuito_abierto = {
    "usuarios": False,
    "mascotas": False
}

tiempo_ultimo_fallo = {
    "usuarios": 0.0,
    "mascotas": 0.0
}     

fallos_maximos = 3

TIEMPO_RECUPERACION = 10

@app.route("/usuarios")
def usuarios():
    print("Accediendo a los usuarios")
    
    if circuito_abierto["usuarios"]:
        tiempo_pasado = time.time() - tiempo_ultimo_fallo["usuarios"]
        if tiempo_pasado >= TIEMPO_RECUPERACION:
            print("Estado HALF-OPEN en usuarios: Intentando recuperar conexión...", flush=True)
        else:
            tiempo_restante = int(TIEMPO_RECUPERACION - tiempo_pasado)
            return {"error": f"Servicio bloqueado. Reintento en {tiempo_restante}s"}, 503
    
    try:
        response = requests.get("http://usuarios:5000/usuarios", timeout=2)
        
        if circuito_abierto["usuarios"]:
            print("Recuperación exitosa. Circuito de usuarios CERRADO.", flush=True)
            
        fallos["usuarios"] = 0
        circuito_abierto["usuarios"] = False
        return jsonify(response.json())
    
    except requests.exceptions.RequestException:
        fallos["usuarios"] += 1
        tiempo_ultimo_fallo["usuarios"] = time.time() 
        print(f"Fallo en usuarios número {fallos['usuarios']}", flush=True)

        if fallos["usuarios"] >= fallos_maximos or circuito_abierto["usuarios"]:
            circuito_abierto["usuarios"] = True
            print("Circuito de usuarios ABIERTO.", flush=True)

        return {"error": "Servicio de usuarios caido"}, 503
    
@app.route("/mascotas")
def mascotas():
    print("Accediendo a las mascotas")
    
    if circuito_abierto["mascotas"]:
        tiempo_pasado = time.time() - tiempo_ultimo_fallo["mascotas"]
        if tiempo_pasado >= TIEMPO_RECUPERACION:
            print("Estado HALF-OPEN en mascotas: Intentando recuperar...", flush=True)
        else:
            tiempo_restante = int(TIEMPO_RECUPERACION - tiempo_pasado)
            return {"error": f"Servicio bloqueado. Reintento en {tiempo_restante}s"}, 503
    
    try:
        response = requests.get("http://backend:5000/mascotas", timeout=2)
        
        if circuito_abierto["mascotas"]:
            print("Recuperación exitosa. Circuito de mascotas CERRADO.", flush=True)
            
        fallos["mascotas"] = 0
        circuito_abierto["mascotas"] = False
        return response.json()
    
    except requests.exceptions.RequestException:
        fallos["mascotas"] += 1
        tiempo_ultimo_fallo["mascotas"] = time.time()
        print(f"Fallo en mascotas número {fallos['mascotas']}", flush=True)

        if fallos["mascotas"] >= fallos_maximos or circuito_abierto["mascotas"]:
            circuito_abierto["mascotas"] = True
            print("Circuito de mascotas ABIERTO.", flush=True)

        return {"error": "Servicio de mascotas no disponible"}, 503

    
@app.route("/mascotas/<int:id>")
def mascota_id(id):
    print("Buscando mascota con id", id)
    
    if circuito_abierto["mascotas"]:
        tiempo_pasado = time.time() - tiempo_ultimo_fallo["mascotas"]
        if tiempo_pasado >= TIEMPO_RECUPERACION:
            print("Estado HALF-OPEN en mascotas (por ID): Intentando recuperar...", flush=True)
        else:
            return {"error": "Servicio bloqueado. Circuito abierto."}, 503
            
    try:
        mascota = requests.get(f"http://backend:5000/mascotas/{id}", timeout=2).json()
        
        if circuito_abierto["mascotas"]:
            print("Recuperación exitosa. Circuito CERRADO.", flush=True)
            
        fallos["mascotas"] = 0
        circuito_abierto["mascotas"] = False
        return jsonify(mascota)   
    
    except requests.exceptions.RequestException:
        fallos["mascotas"] += 1
        tiempo_ultimo_fallo["mascotas"] = time.time()
        print(f"Fallo en mascotas por ID número {fallos['mascotas']}", flush=True)
        
        if fallos["mascotas"] >= fallos_maximos or circuito_abierto["mascotas"]:
            circuito_abierto["mascotas"] = True
            print("Circuito de mascotas ABIERTO.", flush=True)
            
        return {"error": "Servicio de mascotas por id caido"}, 503


@app.route("/resumen")
def resumen():
    print("Resumiendo informacion")
    res_usuarios = {"error": "Servicio no disponible"}
    res_mascotas = {"error": "Servicio no disponible"}

    
    intentar_usuarios = not circuito_abierto["usuarios"] or (time.time() - tiempo_ultimo_fallo["usuarios"] >= TIEMPO_RECUPERACION)
    intentar_mascotas = not circuito_abierto["mascotas"] or (time.time() - tiempo_ultimo_fallo["mascotas"] >= TIEMPO_RECUPERACION)

    if intentar_usuarios:
        try:
            res_usuarios = requests.get("http://usuarios:5000/usuarios", timeout=2).json()
            fallos["usuarios"] = 0
            circuito_abierto["usuarios"] = False
        except requests.exceptions.RequestException:
            fallos["usuarios"] += 1
            tiempo_ultimo_fallo["usuarios"] = time.time()
            if fallos["usuarios"] >= fallos_maximos or circuito_abierto["usuarios"]:
                circuito_abierto["usuarios"] = True

    if intentar_mascotas:
        try:
            res_mascotas = requests.get("http://backend:5000/mascotas", timeout=2).json()
            fallos["mascotas"] = 0
            circuito_abierto["mascotas"] = False
        except requests.exceptions.RequestException:
            fallos["mascotas"] += 1
            tiempo_ultimo_fallo["mascotas"] = time.time()
            if fallos["mascotas"] >= fallos_maximos or circuito_abierto["mascotas"]:
                circuito_abierto["mascotas"] = True

    return jsonify({
        "Usuarios": res_usuarios,
        "Mascotas": res_mascotas
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)