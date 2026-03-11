-- Usamos la base de datos unificada del contenedor
USE tourfer_data;

-- Borramos en orden inverso para no romper llaves foráneas
DROP TABLE IF EXISTS reservas;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS roles;

CREATE TABLE roles (
    id INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

INSERT INTO roles (id, nombre) VALUES
(1, 'Admin'),
(2, 'Cliente');

CREATE TABLE usuarios (
    -- CAMBIO: De SERIAL a INT AUTO_INCREMENT
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rol_id INT NOT NULL DEFAULT 2, 
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);

CREATE TABLE reservas (
    -- CAMBIO: De SERIAL a INT AUTO_INCREMENT
    id INT AUTO_INCREMENT PRIMARY KEY,
    tour_id INT NOT NULL, 
    -- Ahora usuario_id (INT) coincide perfectamente con usuarios(id) (INT)
    usuario_id INT,
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cantidad_personas INT NOT NULL,
    costo_total DECIMAL(10, 2) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'Pendiente' CHECK (estado IN ('Pendiente', 'Confirmada', 'Cancelada')),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Inserción de datos de prueba
INSERT INTO `usuarios` (`id`, `nombre`, `email`, `password`, `fecha_registro`, `rol_id`) VALUES
(101, 'Ana Pérez', 'ana.perez@email.com', '$2b$12$0TPh9qxvO5hO1wVjVHZ.beiYi8AkScl2UOEdGf7xqYlZghWhq7NHW', '2025-11-02 22:46:55', 2),
(102, 'Juan Rodríguez', 'juan.rodriguez@email.com', '$2b$12$wHHKAhXLbDtSBqTkDgGuFujk8OjGHEGnEsF1kTQ11MwUZTBzgCHsm', '2025-11-02 22:46:55', 2),
(103, 'Lucía Gómez', 'lucia.gomez@email.com', '$2b$12$46VNCjur9AUrVEsBOFK98eW0xeZj51UzMycXGSHcy97gYO6i22HD2', '2025-11-02 22:46:55', 2),
(104, 'Manuel Fernandez', 'mf@email.com', '$2b$12$Nw4DS/O2gygau6nA6.hVq.iBb92wk4m1KRY/g বায়ুuKydT52nPt62M52', '2025-11-02 22:46:55', 2),
(105, 'Jose Montenegro', 'jm@email.com', '$2b$12$nKqWAcjelSXRZ9UJDsev7.w21/J1LDU0xwjbVrmJ0510BAMC1Qv6a', '2025-11-02 22:46:55', 1),
(106, 'Felipe', 'felipe@gmail.com', '$2b$12$xW9/hywRjrZEB1pmzz3HTO/TZXDMsmCtYjwET0h63gWYmseBIVVve', '2025-11-02 22:47:57', 1),
(107, 'José Luis', 'joseluis@gmail.com', '$2b$12$KZ6Hf2pjXR/Asu8sKrC9See7JsNhmFiUSWXs4VnHWvC5RXOuu3/aC', '2025-11-03 19:06:04', 1),
(108, 'Dopier', 'dopier@gmail.com', '$2b$12$aolxuTBJixhsP8o0h4wDwuyO5JoVR4iZz6Gmkw2zMJtSiEZhCICPG', '2025-11-08 22:30:16', 2),
(109, 'Dopier', 'dopier123@gmail.com', '$2b$12$EDvHJdBd5EdRR7vCkbSYMOHYiAMn.t2EN1ZNeNWtyGjEoyrXc6cs.', '2025-11-08 22:30:29', 2);

INSERT INTO `reservas` (`id`, `tour_id`, `usuario_id`, `fecha_reserva`, `cantidad_personas`, `costo_total`, `estado`) VALUES
(1, 1, 101, '2025-11-02 22:46:55', 2, 300000.00, 'Confirmada'),
(2, 3, 102, '2025-11-02 22:46:55', 1, 350000.00, 'Confirmada'),
(3, 2, 101, '2025-11-02 22:46:55', 4, 380000.00, 'Pendiente'),
(4, 7, 103, '2025-11-02 22:46:55', 2, 500000.00, 'Confirmada'),
(5, 10, 102, '2025-11-02 22:46:55', 3, 360000.00, 'Cancelada'),
(6, 5, 104, '2025-11-02 22:46:55', 1, 1400000.00, 'Confirmada'),
(7, 8, 105, '2025-11-02 22:46:55', 3, 330000.00, 'Confirmada'),
(8, 11, 101, '2025-11-02 22:46:55', 2, 180000.00, 'Confirmada'),
(9, 15, 104, '2025-11-02 22:46:55', 4, 240000.00, 'Pendiente'),
(10, 6, 102, '2025-11-02 22:46:55', 2, 150000.00, 'Confirmada'),
(11, 14, 103, '2025-11-02 22:46:55', 2, 200000.00, 'Cancelada'),
(12, 1, 105, '2025-11-02 22:46:55', 1, 150000.00, 'Confirmada'),
(13, 11, 101, '2025-11-02 22:53:30', 4, 520000.00, 'Confirmada'),
(14, 5, 101, '2025-11-03 23:08:22', 2, 2800000.00, 'Confirmada');