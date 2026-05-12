# FASE 1 – OBSERVAR (sin modificar código)

## Procedimiento realizado

En esta fase se apagó el servicio de mascotas (backend) y se realizaron varias peticiones al gateway para observar el comportamiento del sistema SIN modificar el código.

## Descripción del procedimiento

**¿Qué comandos ejecutaron para apagar el servicio?**

- `docker-compose up --build`  
  *Se utilizó para construir y levantar todos los servicios del sistema (gateway, backend, usuarios y base de datos).*
- `cd C:\\Users\\Usuario\\Downloads\\pet_shop_clase_sd_g1`  
  *Se utilizó para ubicarse en la carpeta del proyecto antes de ejecutar los contenedores.*
- `docker ps`  
  *Se utilizó para listar los contenedores en ejecución y obtener sus nombres e identificadores.*
- `docker stop pet_shop_clase_sd_g1-backend-1`  
  *Se utilizó para detener el servicio de mascotas (contenido en el backend), simulando una falla del sistema.*
- `docker logs -f pet_shop_clase_sd_g1-gateway-1`  
  *Se utilizó para visualizar los logs del gateway en tiempo real y analizar el comportamiento del sistema frente a la caída del servicio.*

**¿Cuántas peticiones hicieron al gateway y a qué endpoint?**

Se realizaron un total de 7 peticiones al gateway, específicamente al endpoint `/mascotas`, con el objetivo de observar el comportamiento del sistema ante la caída del servicio.

## Análisis de los logs

**¿Qué mostraron los logs del gateway durante las peticiones?**

**Fallo número 1**
```
172.20.0.1 - - [06/May/2026 03:18:20] "GET /mascotas HTTP/1.1" 503 - 172.20.0.1 - - [06/May/2026 03:18:21] "GET /favicon.ico HTTP/1.1" 404 -
```

**Fallo número 2**
```
172.20.0.1 - - [06/May/2026 03:30:31] "GET /mascotas HTTP/1.1" 503 - 172.20.0.1 - - [06/May/2026 03:30:31] "GET /favicon.ico HTTP/1.1" 404 -
```

**Fallo número 3 Circuito abierto**
```
172.20.0.1 - - [06/May/2026 03:30:39] "GET /mascotas HTTP/1.1" 503
- 172.20.0.1 - - [06/May/2026 03:30:39] "GET /favicon.ico HTTP/1.1" 404
- 172.20.0.1 - - [06/May/2026 03:30:41] "GET /mascotas HTTP/1.1" 503
- 172.20.0.1 - - [06/May/2026 03:30:41] "GET /favicon.ico HTTP/1.1" 404
- 172.20.0.1 - - [06/May/2026 03:32:11] "GET /mascotas HTTP/1.1" 503
- 172.20.0.1 - - [06/May/2026 03:32:11] "GET /favicon.ico HTTP/1.1" 404
- 172.20.0.1 - - [06/May/2026 03:32:12] "GET /mascotas HTTP/1.1" 503
- 172.20.0.1 - - [06/May/2026 03:32:12] "GET /favicon.ico HTTP/1.1" 404
- 172.20.0.1 - - [06/May/2026 03:32:38] "GET /mascotas HTTP/1.1" 503
- 172.20.0.1 - - [06/May/2026 03:32:38] "GET /favicon.ico HTTP/1.1" 404 -
```

**📸 Evidencia – fase1.png**

<img width="975" height="451" alt="imagen" src="https://github.com/user-attachments/assets/7e85323a-aba7-4d60-bd0e-fb27579322f1" />


## Respuestas requeridas

**¿Qué hace el sistema actualmente cuando el servicio de mascotas falla?**

**Respuesta:**

Cuando el servicio de mascotas falla, el sistema inicialmente intenta procesar las peticiones, pero a partir de tres intentos en esta caso, deja de realizar llamadas al servicio. En ese punto, el sistema comienza a responder de forma inmediata al cliente con un mensaje indicando que el servicio se encuentra temporalmente bloqueado.

**¿Se protege el sistema o insiste en conectarse?**

**Respuesta:**

El sistema se protege. Inicialmente intenta conectarse al servicio, pero después de varios fallos consecutivos abre el circuito y deja de hacer peticiones, respondiendo inmediatamente al usuario.

# FASE 2 – APLICAR (Extensión del Circuit Breaker)

En esta fase se aplica el patrón Circuit Breaker al endpoint /usuarios y a cualquier otro endpoint del gateway, adaptando la lógica (no copiando el código).

## Decisiones de diseño tomadas

**¿Cada servicio tiene su propio contador de fallos?**

**Decisión y justificación:**

Sí, se utilizaron variables separadas por servicio, por ejemplo, fallos_backend y fallos_usuarios

Esto se hizo para que cada servicio maneje sus propios errores de forma independiente. De esta manera, si uno falla, no afecta el funcionamiento de los demás.

La principal ventaja es que el sistema sigue operando parcialmente, mejorando su disponibilidad y control de fallos.

**¿El circuito se abre de forma independiente por servicio?**

**Decisión y justificación:**

Sí, el circuito se abre de forma independiente por cada servicio.

Si el servicio de mascotas (backend) falla, únicamente se abre su circuito y se bloquean sus peticiones, mientras que el servicio de usuarios continúa funcionando con normalidad.

Esto se debe a que, aunque los servicios comparten la misma lógica de programación, cada uno maneja su propio estado (contador de fallos y circuito).

Se eligió este enfoque porque el sistema está basado en microservicios, donde cada servicio debe ser independiente. Esto permite que el sistema siga operando parcialmente y mejora la disponibilidad general.

**¿Qué pasa si falla un servicio pero el otro sigue funcionando?**

**Respuesta y evidencia:**

Se realizó la prueba apagando únicamente el servicio de mascotas (backend).

Al hacer peticiones:

- Al endpoint /mascotas: responde con un error indicando que el servicio no está disponible o que se encuentra bloqueado (circuito abierto).
- Al endpoint /usuarios: responde correctamente, mostrando la lista de usuarios sin ningún problema.

Adicionalmente, al consultar el endpoint `/resumen`, se observa que:
- La información de usuarios se muestra normalmente.
- El servicio de mascotas aparece con un mensaje de error.
- Se incluye un mensaje general indicando que uno o más servicios no están disponibles.

## Código implementado

**Fragmento clave del nuevo código del gateway (endpoint /usuarios con Circuit Breaker):**

```python
def ejecutar_con_circuit_breaker(url, fallos, circuito_abierto, nombre_servicio):
    # CIRCUITO ABIERTO
    if circuito_abierto:
        print(f"[CB] {nombre_servicio}: circuito abierto", flush=True)
        return (
            {"error": f"Servicio '{nombre_servicio}' temporalmente bloqueado"},
            503, fallos, circuito_abierto
        )
    try:
        response = requests.get(url, timeout=2)
        print(f"[CB] {nombre_servicio}: respuesta exitosa", flush=True)
        # Reinicia contador si funcionó
        return (
            response.json(),
            200, 0,
            False
        )
    except Exception as e:
        fallos += 1
        print(f"[CB] {nombre_servicio}: fallo #{fallos} -> {e}", flush=True)
        if fallos >= UMBRAL_FALLOS:
            circuito_abierto = True
            print(f"[CB] {nombre_servicio}: circuito ABIERTO", flush=True)
        return (
            {"error": f"Fallo de conexión con el servicio '{nombre_servicio}'"},
            500, fallos, circuito_abierto
        )
```

**📸 Evidencia – fase2.png**

<img width="975" height="410" alt="imagen" src="https://github.com/user-attachments/assets/eae0b919-0059-452e-ab12-1d386e5b9b84" />


## Observaciones

**¿Qué diferencias notaron entre la lógica de /mascotas y la nueva implementación de /usuarios?**

La principal diferencia es que antes la lógica del Circuit Breaker estaba escrita directamente en el endpoint `/mascotas`, mientras que en `/usuarios` se reutiliza mediante una función. Esto evita duplicar código, mejora la organización y facilita agregar nuevos endpoints manteniendo la independencia de cada servicio.

# FASE 3 – INVESTIGAR (Half-Open)

En esta fase se investiga el concepto de estado 'half-open' del patrón Circuit Breaker.

## Investigación teórica

**¿Qué significa el estado 'half-open'?**

**Definición con sus propias palabras:**

El estado “half-open” (semi-abierto) ocurre cuando, después de que el circuito ha estado abierto por fallos, el sistema decide hacer una petición de prueba para verificar si el servicio ya se ha recuperado.

Se entra a este estado después de un tiempo de espera, cuando el sistema intenta nuevamente comunicarse con el servicio.
**Diferencia entre estados:**

- **CLOSED (cerrado):** el sistema funciona normalmente y las peticiones se realizan sin restricción.
- **OPEN (abierto):** el sistema bloquea las peticiones porque el servicio ha fallado varias veces.
- **HALF-OPEN (semi-abierto):** el sistema permite una petición de prueba para verificar si el servicio vuelve a estar disponible.

**¿Cuándo se vuelve a intentar una llamada?**

**Explicación del mecanismo de recuperación:**

En esta fase se definió conceptualmente un tiempo de espera de 5 segundos para el intento de recuperación, el cual será implementado en la siguiente fase.

**¿Qué pasa si el servicio vuelve a fallar en estado half-open?**

**Comportamiento esperado:**

En estado half-open, si la prueba falla el circuito se vuelve a abrir; si funciona, se cierra. En este caso se realiza un solo intento de prueba.

**📸 Evidencia – fase3.png**

<img width="975" height="367" alt="imagen" src="https://github.com/user-attachments/assets/01dddc05-db17-4d77-a0d3-80020e686725" />


# FASE 4 – IMPLEMENTAR (Recuperación / Half-Open)

En esta fase se implementa la lógica de recuperación con estado half-open en el sistema.

## Parámetros de configuración elegidos

**Tiempo de espera definido (cooldown/recovery timeout):**

Se definió un tiempo de espera de 10 segundos antes de volver a intentar la conexión con el servicio.

Este valor permite dar tiempo suficiente para que el servicio se recupere, evitando intentos constantes que podrían generar más fallos o sobrecarga.

## Lógica implementada

**Espera controlada**

**¿Cómo implementaron el timer de espera?**

Se utilizó la función `time.time()` para manejar el tiempo de espera del Circuit Breaker.

Cuando el circuito pasa a estado OPEN, se guarda el momento exacto en el que ocurrió el fallo (tiempo_apertura). Luego, en cada nueva petición, se calcula cuánto tiempo ha pasado comparando el tiempo actual con ese valor.

**Nuevo intento de conexión (transición a half-open)**

**¿Cómo hacen el intento de prueba?**

El intento de prueba se realiza cuando el circuito pasa de estado OPEN a HALF-OPEN después de cumplirse el tiempo de espera. En ese momento se permite una petición al servicio para verificar si ya se recuperó.

Se distingue de una petición normal porque el estado del circuito es HALF-OPEN. Si la petición es exitosa, el circuito se cierra; si falla, se vuelve a abrir.

**Decisión: cerrar o re-abrir el circuito**

**Flujo de decisión implementado:**

Cuando el circuito está en estado HALF-OPEN, se realiza una petición de prueba al servicio:

SI el intento de prueba TIENE ÉXITO:
→ Se reinicia el contador de fallos 
→ El circuito pasa a estado CLOSED
→ El sistema vuelve a operar con normalidad 

SI el intento de prueba FALLA:
→ El circuito vuelve a estado OPEN
→ Se registra el momento del fallo 
→ Se bloquean nuevamente las peticiones hasta el siguiente intento

## Código completo de recuperación

**Fragmento del gateway con la lógica half-open implementada:**

```python
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
```

**📸 Evidencia – fase4.png**

<img width="975" height="692" alt="imagen" src="https://github.com/user-attachments/assets/9f5692b1-40da-4eb7-8005-548ac4064026" />


# FASE 5 – VALIDAR

En esta fase se prueba el sistema en 4 escenarios distintos para validar el comportamiento completo del Circuit Breaker.

## Escenario 1: Servicio funcionando normalmente

**Procedimiento:**

Al ejecutar las peticiones a los endpoints /mascotas y /usuarios, el sistema responde correctamente mostrando la información esperada de cada servicio.

En el endpoint /resumen, se puede observar que ambos servicios retornan datos válidos y no se presentan errores. Además, el estado de los circuitos se mantiene en CLOSED, lo que indica que no hay fallos y el sistema está funcionando con normalidad.

**📸 Evidencia – fase5a.png**

<img width="783" height="522" alt="imagen" src="https://github.com/user-attachments/assets/0013998f-028d-41a2-aa59-ccf4904adc4a" />


## Escenario 2: Servicio caído

**Procedimiento:**

**¿Cuándo se abre el circuito?**
El circuito se abre cuando el número de fallos alcanza el umbral definido (en este caso, 3 fallos). A partir de ese momento, el sistema deja de intentar conectarse al servicio.

**¿Qué respuesta recibe el cliente?**

- *Primeras peticiones (antes del umbral):* el cliente recibe errores de conexión (500), ya que el sistema intenta acceder al servicio pero falla.
- *Después de alcanzar el umbral:* el circuito se abre y el cliente recibe una respuesta más rápida indicando que el servicio está bloqueado o no disponible (503), sin intentar nuevamente la conexión.

**📸 Evidencia – fase5b.png**

<img width="975" height="381" alt="imagen" src="https://github.com/user-attachments/assets/a90500c1-ddee-4a67-a498-93421e6b7f2b" />


## Escenario 4: Recuperación del servicio

**Procedimiento:**

El circuito se cerró correctamente después de que el servicio de mascotas volvió a levantarse en Docker. Luego de esperar los 10 segundos configurados como tiempo de recuperación, el gateway realizó un nuevo intento de conexión en estado HALF-OPEN. Como el servicio respondió correctamente, el circuito cambió nuevamente a estado CLOSED y el sistema volvió a funcionar normalmente sin necesidad de reiniciar el gateway.

**📸 Evidencia – fase5d.png**

<img width="975" height="483" alt="imagen" src="https://github.com/user-attachments/assets/fe63f3b2-ebc0-4a52-8a9d-a7e43c4e22aa" />
