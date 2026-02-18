# Arquitectura del Sistema: TourFer

**Integrantes:**
* José Luis Montenegro
* Manuel Felipe Fernández
* Jose Hebert Aponza

---

## PARTE 1 — Entender el problema

### ¿Qué problema resuelve el sistema?
TourFer buscar centralizar la oferta turística que actualmente se encuentra algo dispersa, permitiendo a los usuarios encontrar, comparar y reservar tours de forma digital, todo en un solo lugar.

### ¿Quién lo usará?
1.  **Turistas:** Usuarios nacionales e internacionales que buscan reservar experiencias.
2.  **Proveedores Turísticos:** Proveedores locales que necesitan una herramienta para cargar su inventario y gestionar ventas.
3.  **Administradores:** Personal técnico encargado de la supervisión de la plataforma y moderación.

### ¿Qué pasaría si no existiera?
La reserva de tours seguiría siendo un proceso manual, propenso a errores de disponibilidad y con poca visibilidad para los pequeños proveedores, perdiendo así oportunidades económicas frente a las grandes agencias internacionales, además, los turistas tendrían dificultades para encontrar opciones seguras. 

---
## PARTE 2 – Identificar los servicios

### Funciones principales del sistema
* Registro y validación de usuarios con permisos diferenciados mediante roles.
* Visualización de paquetes, filtrado por precio/ubicación y visualización de disponibilidad en tiempo real.
* Gestión de ciclo de vida de una reserva, desde la selección de fecha, hasta la confirmación de pago
* Herramientas para que los proveedores de los tours puedan subirlos, gestionarlos y ver estadísticas básicas de sus ventas.

### Descomposición en Servicios Independientes
Para garantizar la independencia técnica y facilitar el desarrollo en equipo, el sistema se divide en:
1.  **Servicio de Autenticación:** Gestión de seguridad, contraseñas y generación de tokens JWT.
2.  **Servicio de Catálogo:** CRUD de paquetes turísticos, manejo de imágenes y metadatos.
3.  **Servicio de Reservas:** Encargado de la lógica de negocio para transacciones y bloqueos de cupos.
4.  **Servicio de Notificaciones:** Envío de correos electrónicos de confirmación y alertas.


### Procesos independientes
* La visualización y búsqueda en el catálogo es un proceso de lectura que no requiere autenticación.
* El envío del correo de confirmación es independiente de la transacción, puesto que si el servidor de correos falla, la reserva sigue siendo válida en la base de datos.

---
## PARTE 3 — Comunicación entre servicios

### ¿Qué servicio necesita información de otro?
* El servicio de reservas solicita la validación del token JWT del usuario para permitir la transacción.
* El motor de reservas solicita al catálogo la validación de cupos disponibles y el precio vigente antes de confirmar la compra.
* El catálogo solicita validación de rol de "Proveedor" o "Admin" antes de permitir la subida o edición de un paquete.

### ¿Quién solicita datos?
* El servicio de reservas actúa como el solicitante principal en el flujo de compra.
* El servicio de catálogo solicita datos de validación en la gestión de tours.

### ¿Quién responde?
* El servicio de usuarios responde confirmando la autenticidad de la cuenta que realiza la compra, o que desea gestionar los tours.
* El servicio de tours responde confirmando la disponibilidad y el precio final.

---
## PARTE 4 — Elección de Arquitectura

Se ha seleccionado una arquitectura de **Microservicios** basada en los siguientes criterios:

* El sistema busca estar diseñado para una audiencia masiva que incluye turistas nacionales e internacionales, además de diversos proveedores turísticos locales, se proyecta una concurrencia de cientos a miles de usuarios activos simultáneamente, aunque esto dependería de la temporada.
* El sistema debe ser escalable, puesto que, debe ser capaz de soportar incrementos repentinos de tráfico durante épocas de vacaciones o festividades, sin que afecte la disponibilidad de los servicios básicos.
* Al ser considerado como un sistema de tamaño mediano a grande, puesto que, no es una simple aplicación monolítica, sino que requiere la interacción de al menos cuatro servicios independientes (autenticación, tours, reservas y notificaciones) para completar su flujo de valor.
  
### Justificación
Elegimos esta arquitectura porque permite escalar cada parte de TourFer de forma independiente, ya que, por ejemplo, si en temporada alta hay muchas consultas de tours pero pocas compras, podemos escalar solo el servicio de tours sin afectar el resto

---
## PARTE 5 — Base de Datos

### ¿Qué información debe guardarse?
* Datos de usuario
* Detalles de tours
* Historial de reservas y pagos.
  
### ¿Qué datos son críticos?
* El historial de transacciones
* La información privada de los clientes

### ¿Qué pasaría si se pierden?
Su pérdida implicaría problemas legales y financieros, además de la pérdida de la credibilidad y confianza por parte de todos los usuarios.

---
### ¿Quién usará el sistema?
* Cliente.
* Proveedor.
* Administrador.

### ¿Todos pueden hacer lo mismo?
No, los administradores tienen acceso global para moderación, gestión de usuarios y auditoría técnica del sistema, los proveedores solo tienen permisos para gestionar su propio inventario y visualizar sus métricas de ventas, y los clientes acceso únicamente para la lectura del catálogo y creación de reservas propias.

---

