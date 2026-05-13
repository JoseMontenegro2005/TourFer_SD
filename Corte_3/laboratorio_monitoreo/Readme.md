# Taller Práctico: Sistema de Pedidos Distribuido y Monitoreo

**Integrantes:**
* Manuel Felipe Fernández
* Jose Luis Montenegro

## 1. Arquitectura del Sistema

El proyecto implementa una arquitectura basada en microservicios utilizando contenedores. El ecosistema está compuesto por cuatro servicios principales desarrollados en Python con el framework Flask, los cuales se orquestan y comunican a través de una red interna de Docker Compose.

Los componentes del sistema son:

* **Servicio de Pedidos (Puerto interno 5000):** Gestiona la información de las órdenes de los clientes.
* **Servicio de Inventario (Puerto interno 5000):** Controla el stock de los productos disponibles.
* **Servicio de Pagos (Puerto interno 5000):** Administra el estado de las transacciones.
* **API Gateway (Puerto externo 5000):** Actúa como el único punto de entrada para los clientes. Su función es enrutar las peticiones hacia los microservicios correspondientes, agrupar las respuestas y manejar los fallos de red para evitar que el sistema completo colapse si un servicio interno se desconecta.

La comunicación entre el Gateway y los microservicios se realiza de forma síncrona mediante peticiones HTTP GET. Para fines prácticos de este laboratorio, los datos se manejan en memoria utilizando estructuras JSON estáticas, sin requerir bases de datos externas.
<p align="center">
  <img width="1637" height="872" alt="mermaid-diagram-2026-05-12-235252" src="https://github.com/user-attachments/assets/87cf0d9e-63c9-4044-81ae-e0cf31855e02" />
</p>

## 2. Monitoreo Implementado

El sistema cuenta con una estrategia de observabilidad distribuida en múltiples fases para garantizar el control sobre la salud de la aplicación.

* **Logs Descriptivos (Fase 1):** Se implementó un registro de eventos estándar en la consola del Gateway. Cada petición registra el inicio de la transacción, el tiempo exacto que tardó en resolverse y, en caso de fallo, emite una advertencia detallada.
* **Health Checks (Fase 2):** Se diseñó el endpoint `/estado` en el Gateway. Este se encarga de hacer ping a la ruta individual de estado de cada microservicio para validar su disponibilidad operativa en tiempo real.
* **Monitoreo General (Fase 3):** A través del endpoint `/resumen`, el Gateway realiza consultas concurrentes a todos los servicios y unifica la información de negocio en una sola carga útil, permitiendo observar el panorama completo de los datos.
* **Métricas de Rendimiento (Fase 5):** 
    * **Tiempos de respuesta:** Se utiliza la librería nativa de tiempo para calcular la latencia de cada solicitud HTTP entre el Gateway y las APIs internas.
    * **Cantidad de errores:** Se configuró un diccionario en la memoria del Gateway que actúa como un contador global, incrementando su valor cada vez que un bloque de excepción captura una petición fallida.

## 3. Resultados Observados y Simulación de Fallos

Para evaluar la resiliencia de la arquitectura, se procedió a ejecutar la simulación de apagado forzado del servicio de pagos (Fase 4).

### Disponibilidad
Al detener el contenedor de pagos, el sistema demostró tolerancia a fallos. El API Gateway no colapsó; en su lugar, capturó la excepción de tiempo de espera y retornó un código de estado 503 controlado para la sección de pagos, mientras que los servicios de pedidos e inventario continuaron entregando su información con normalidad en los endpoints `/resumen` y `/estado`.
<p align="center">
  <img width="592" height="204" alt="imagen" src="https://github.com/user-attachments/assets/f902b78a-e7d9-42f6-96db-8ccf224bc317" />
<br><br>
  <img width="452" height="182" alt="imagen" src="https://github.com/user-attachments/assets/d47e5f0d-33fd-4f22-ada3-3d52dd03ad78" />
<br><br>
  <img width="525" height="52" alt="imagen" src="https://github.com/user-attachments/assets/94499b42-ef43-4370-bf43-9b5dca08269c" />
</p>

Si se recarga la pagina, el contador de errores incrementará

<p align="center">
  <img width="575" height="139" alt="imagen" src="https://github.com/user-attachments/assets/9317475f-7c3a-4ac8-be3d-38ab5d757d70" />
</p>

Al ingresar al endpoint `/estado` se incrementará nuevamente una unidad su valor

<br>
<p align="center">
  <img width="413" height="330" alt="imagen" src="https://github.com/user-attachments/assets/6b5fbaa6-e736-4697-84fe-e4925798701b" />
</p>
<br>
<p align="center">
  <img width="575" height="103" alt="imagen" src="https://github.com/user-attachments/assets/825ede12-5d61-4097-991b-ec6c540372e5" />
</p>
<br>
<br>

Lo mismo sucedería en el endpoint `/resumen`

<br>
<p align="center">
  <img width="483" height="674" alt="imagen" src="https://github.com/user-attachments/assets/26cc18e6-e40b-4bff-9195-4dc23462f4e1" />
</p>
<br>
<p align="center">
  <img width="574" height="106" alt="imagen" src="https://github.com/user-attachments/assets/5b2023e1-c001-4df2-b843-2dba997818c8" />
</p>

### Análisis de Logs y Errores
Tras múltiples peticiones manuales durante el fallo inducido, la consola del contenedor Gateway registró correctamente el incremento en las métricas de error. Se observó cómo el diccionario interno contabilizaba de forma precisa cada solicitud rechazada, reflejando el total acumulado en los logs de advertencia.

<p align="center">
  <img width="542" height="113" alt="imagen" src="https://github.com/user-attachments/assets/ed7d3ace-614f-44eb-ab8f-bf46af4b53e9" />
</p>
