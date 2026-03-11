-- =================================================================
-- Script de Configuración Inicial para el Proyecto TourFer
-- Ejecutar este script UNA SOLA VEZ para preparar el entorno.
-- =================================================================

-- --- 1. Creación de Usuarios y Permisos ---

-- Se eliminan los usuarios si ya existen para una instalación limpia
DROP USER IF EXISTS 'user_catalogo'@'localhost';
DROP USER IF EXISTS 'user_reservas'@'localhost';

-- Se crean los usuarios con sus respectivas contraseñas
CREATE USER 'user_catalogo'@'localhost' IDENTIFIED BY 'tourpass123';
CREATE USER 'user_reservas'@'localhost' IDENTIFIED BY 'reservaspass456';

-- --- 2. Creación de Bases de Datos ---

-- Se eliminan las bases de datos si ya existen para evitar conflictos
DROP DATABASE IF EXISTS catalogo_db;
DROP DATABASE IF EXISTS reservas_db;

CREATE DATABASE catalogo_db;
CREATE DATABASE reservas_db;

-- --- 3. Asignación de Permisos ---

-- Se asignan todos los privilegios a cada usuario sobre su base de datos
GRANT ALL PRIVILEGES ON catalogo_db.* TO 'user_catalogo'@'localhost';
GRANT ALL PRIVILEGES ON reservas_db.* TO 'user_reservas'@'localhost';

-- Se aplican los cambios para que MySQL los reconozca
FLUSH PRIVILEGES;

-- --- Fin del Script ---