-- Crear tabla de mascotas
CREATE TABLE IF NOT EXISTS mascotas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos de prueba
INSERT INTO mascotas (nombre, tipo) VALUES 
('Max', 'Perro'),
('Mittens', 'Gato'),
('Tweety', 'Pajaro');
