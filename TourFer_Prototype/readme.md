# TourFer: Sistema de Gestión de Reservas de Tours (Avance 2)

## 1. Descripción del Proyecto

TourFer es una plataforma distribuida diseñada para la gestión de servicios turísticos en Colombia. El sistema emplea una arquitectura de microservicios para garantizar la escalabilidad, el mantenimiento independiente y el aislamiento de datos. Cada módulo del sistema opera como un servicio autónomo con su propia lógica de negocio y persistencia de datos.

### Componentes Principales:
   * **Microservicio de Usuarios:** Gestiona el registro, autenticación (JWT) y perfiles de los clientes y administradores.

   * **Microservicio de Catálogo (Tours):** Administra la oferta de tours, destinos y disponibilidad en tiempo real.

   * **Microservicio de Reservas:** Coordina el proceso de compra, validando cupos contra el catálogo y persistiendo el historial de transacciones.

### Arquitectura Técnica:

   * **Backend:** Flask (Python 3.11).

   * **Base de Datos:** MySQL 8.0 con aislamiento físico (bases de datos independientes).

   * **Comunicación:** RESTful API mediante el protocolo HTTP.

   * **Orquestación:** Docker y Docker Compose.

## 2. Instrucciones de Ejecución

### Requisitos Previos:

   * Docker Desktop instalado.

   * Docker Compose habilitado.

### Pasos para el Despliegue:

   * **Configuración del Entorno:**
    Asegúrese de contar con un archivo .env en la raíz del proyecto para gestionar credenciales y URLs de comunicación. Siga estos pasos para configurarlo:

      1. Localice el archivo .env.example en la raíz del proyecto.

      2. Cree una copia de este archivo y renómbrela como .env

      3. Verifique que los valores en .env coincidan con los definidos en setup_database.sql (especialmente las contraseñas de los usuarios de la base de datos).

      4. Asegúrese de que las URLs de los microservicios apunten a los nombres de los servicios de Docker (ej. http://tourfer-catalogo:5000).

   * **Limpieza de Volúmenes (Recomendado):**
    Para asegurar una carga limpia de los esquemas de base de datos, ejecute:
   
   ```bash
   docker-compose down -v
   ```

   * **Construcción e Inicio:**
    Ejecute el siguiente comando para construir las imágenes y levantar los servicios:
    
   ```bash
    docker-compose up --build 
   ```

   * **Verificación:**

   Puede monitorear el estado de la base de datos y la ejecución de los scripts de inicialización con:

   ```bash
   docker logs -f tourfer-db
   ```


## 3. Descripción de Endpoints

### Microservicio de Usuarios (Puerto 5003)

**Gestiona la identidad de los usuarios del sistema.**

   * **POST /register:** Registra un nuevo usuario en la base de datos.

   * **POST /login:** Autentica al usuario y devuelve un Access Token (JWT).

     
### Microservicio de Catálogo (Puerto 5001)

**Mantiene la información técnica de los paquetes turísticos.**

   * **GET /tours:** Retorna el listado completo de tours disponibles.

   * **GET /tours/id_tour:** Retorna el detalle de un tour específico.
     
   * **GET /guia:** Retorna el listado completo de guias disponibles. 

     
### Microservicio de Reservas (Puerto 5002)

**Orquestador de la lógica de negocio de compra.**

   * **POST /reservas:** (Protegido por JWT) Crea una nueva reserva.

       Consulta disponibilidad al Catálogo vía HTTP.

       Si hay cupos, inserta la reserva en la base de datos local.

       Solicita al Catálogo la actualización (decremento) de cupos disponibles.

   *  **GET /mis-reservas:** Retorna el historial de reservas del usuario en sesión.
     

## 4. Estructura de Datos y Persistencia

El sistema utiliza un contenedor único de MySQL que gestiona tres esquemas independientes mediante scripts de inicialización automatizada:

   * **usuarios_db:** Tablas usuarios y roles.

   * **catalogo_db:** Tablas tours, y guias.

   * **reservas_db:** Tabla reservas.

La persistencia está garantizada mediante un volumen nombrado de Docker (db_data), lo que permite que la información prevalezca tras el reinicio de los contenedores.

## 5. Integración de Servicios

La comunicación entre microservicios se realiza de forma síncrona mediante peticiones HTTP. El servicio de Reservas actúa como cliente del servicio de Catálogo, implementando lógica para asegurar que no se confirmen reservas sin la actualización correspondiente en el inventario del catálogo.

## 6. Guía de Pruebas y Validación

Actualmente el proyecto TourFer cuenta con los 7 endpoints mencionados previamente, para usar cualquiera del microservicio del catalogo se puede hacer desde el navegador o usando Postman, pero para los otros 2, se recomienda Postman o alguna alternativa que ofrezca resultados similares.

   1. Para empezar se recomienda acceder a http://127.0.0.1:5001/tours desde cualquier navegador para confirmar que la base de datos de catálogo cargó exitosamente.

   2. Utilice Postman para registrar un usuario accediendo en http://127.0.0.1:5003/register haciendo una petición POST con un Body (JSON): {"nombre": "Nombre", "email": "correo@ejemplo.com", "password": "123"}

   3. Una vez registrado, se debe realizar el login accediendo en http://127.0.0.1:5003/login haciendo una petición POST con un Body (JSON): {"email": "correo@ejemplo.com", "password": "123"} estoy dará como respuesta un Token que se debe copiar para realizar el proceso de reservas.

   4. Una vez copiado el Token se debe ir al apartado de Auth o autorización y selecionando la opción Bearer Token se pega dicho Token

   5. A continuación ya podremos probar el servicio de reservas accediendo a http://127.0.0.1:5002/reservas haciendo una petición POST con un Body (JSON): {"tour_id": int, "cantidad_personas": int} el tour_id se obtiene en el servicio de catalogo en el paso 1

   6. Al hacer la anterior petición debe salir un mensaje de exito 200, confirmando la reserva (o uno de error en caso de que la cantidad de personas sea superior a la cantidad disponible), y si se recarga la pagina http://127.0.0.1:5001/tours se podrá observar que el tour usado en el paso anterior, se habrá actualizado la cantidad de personas.