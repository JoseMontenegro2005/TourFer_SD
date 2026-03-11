# Prototipo Técnico Inicial - TourFer (Avance 1)

Este repositorio contiene el prototipo funcional de la arquitectura distribuida para el proyecto **TourFer**, implementado con contenedores de Docker.

## Arquitectura del Prototipo
El sistema está diseñado bajo el patrón de Microservicios y demuestra el concepto de *Database-per-Service* de forma lógica, así como la comunicación síncrona inter-servicios.

Consta de 3 contenedores principales:
1. **tourfer-db (MySQL 8.0):** Base de datos unificada que inicializa automáticamente los esquemas y datos semilla (seeds) mediante volúmenes montados. Cuenta con *Healthchecks* para garantizar resiliencia.
2. **tourfer-catalogo (Flask):** Servicio expuesto en el puerto `5001` que gestiona la lógica de los tours y guías.
3. **tourfer-reservas (Flask):** Servicio expuesto en el puerto `5002` que gestiona las transacciones de los usuarios. Se comunica internamente a través de la red de Docker (`tourfer_net`) con el Catálogo para validar la existencia de tours.

## Requisitos Previos
* Tener instalado [Docker Desktop](https://www.docker.com/products/docker-desktop/).
* Asegurarse de tener libres los puertos `5001`, `5002` y `3306` en el equipo host.

## Instrucciones de Ejecución

1. Abre una terminal en la carpeta raíz del proyecto (donde se ubica el archivo `docker-compose.yml`).
2. Ejecuta el siguiente comando para construir las imágenes y levantar la arquitectura en segundo plano:
   ```bash
   docker-compose up -d --build
3. Espera aproximadamente 15 segundos a que el motor de MySQL finalice su inicialización y ejecute los scripts SQL. Puedes verificar que todo está listo ejecutando:
   ```bash
   docker-compose ps

## Pruebas de Funcionamiento
Una vez que los servicios estén inicializados, puedes probar la comunicación entre ellos usando tu navegador o Postman:
GET http://localhost:5002/public/tours aqui se prueba el funcionamiento del servicio de Reservas, el cual hace una petición HTTP interna hacia el servicio de Catálogo para traerte los datos.
Acceso directo a Catálogo:
    GET http://localhost:5001/tours

Si se quiere realizar un prueba más profunda, se recomienda hacer en postman la siguiente prueba:

Para registrarse usar:

   POST http://localhost:5002/register

Y en body poner los siguientes datos:
{
   "nombre": "su nombre",
"email": "su correo",
"password": "su contraseña";
}

Saldra un mensaje de registro exitoso, luego se debe hacer login usando:

   POST http://localhost:5002/login

Y en body poner los siguientes datos:
{
"email": "su correo registrado",
"password": "su contraseña registrada"}

Al enviar la peticion regresará un token, se debe copiar dicho token y ponerlo en Auth / autorizacion, en Auth Type se pone Bearer Token y se pega el respectivo token.

A partir de ahora ya se pueden hacer reservas, o revisar reservas.

## Detener la Arquitectura
Para apagar los contenedores y destruir los volúmenes temporales de la base de datos (ideal para reiniciar desde cero con datos limpios), ejecuta:
   ```bash
   docker-compose down -v
