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
