-- FoodDash Seed Data for MySQL
-- Sample data for testing and development

-- =============================================
-- CATEGORIES
-- =============================================
INSERT INTO categories (id, name, icon, display_order) VALUES
    ('c1000001-0000-0000-0000-000000000001', 'Comida Rápida', 'burger', 1),
    ('c1000001-0000-0000-0000-000000000002', 'Pizza', 'pizza', 2),
    ('c1000001-0000-0000-0000-000000000003', 'Saludable', 'salad', 3),
    ('c1000001-0000-0000-0000-000000000004', 'Asiática', 'noodles', 4),
    ('c1000001-0000-0000-0000-000000000005', 'Mexicana', 'taco', 5),
    ('c1000001-0000-0000-0000-000000000006', 'Postres', 'cake', 6),
    ('c1000001-0000-0000-0000-000000000007', 'Cafetería', 'coffee', 7),
    ('c1000001-0000-0000-0000-000000000008', 'Colombiana', 'pot', 8);

-- =============================================
-- TEST USER (password: test123)
-- =============================================
INSERT INTO users (id, email, password_hash, full_name, phone) VALUES
    ('u1000001-0000-0000-0000-000000000001', 
     'test@fooddash.com', 
     '$2b$10$rQZ8K5YJKgX8K5YJKgX8Ku5YJKgX8K5YJKgX8K5YJKgX8K5YJKgX', 
     'Usuario de Prueba', 
     '+57 300 123 4567');

INSERT INTO user_addresses (id, user_id, label, street_address, city, is_default) VALUES
    ('a1000001-0000-0000-0000-000000000001',
     'u1000001-0000-0000-0000-000000000001',
     'Casa',
     'Calle 100 #15-25, Apto 501',
     'Bogotá',
     TRUE);

-- =============================================
-- RESTAURANTS
-- =============================================
INSERT INTO restaurants (id, name, description, image_url, cuisine_type, rating, total_reviews, delivery_time_min, delivery_time_max, delivery_fee, is_featured) VALUES
    ('r1000001-0000-0000-0000-000000000001', 
     'Burger Palace', 
     'Las mejores hamburguesas artesanales de la ciudad con ingredientes premium',
     'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800',
     'Comida Rápida',
     4.8, 234, 20, 35, 5000, TRUE),
     
    ('r1000001-0000-0000-0000-000000000002', 
     'Pizza Roma', 
     'Auténtica pizza italiana horneada en horno de leña',
     'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800',
     'Pizza',
     4.6, 189, 25, 40, 4500, TRUE),
     
    ('r1000001-0000-0000-0000-000000000003', 
     'Green Bowl', 
     'Bowls saludables y ensaladas frescas para una vida equilibrada',
     'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800',
     'Saludable',
     4.7, 156, 15, 30, 3500, TRUE),
     
    ('r1000001-0000-0000-0000-000000000004', 
     'Sushi Master', 
     'El mejor sushi con pescado fresco importado diariamente',
     'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800',
     'Asiática',
     4.9, 312, 30, 45, 6000, TRUE),
     
    ('r1000001-0000-0000-0000-000000000005', 
     'Taco Loco', 
     'Tacos auténticos mexicanos con recetas tradicionales',
     'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800',
     'Mexicana',
     4.5, 98, 20, 35, 4000, FALSE),
     
    ('r1000001-0000-0000-0000-000000000006', 
     'La Cazuela Criolla', 
     'Comida colombiana tradicional como la de la abuela',
     'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800',
     'Colombiana',
     4.7, 267, 25, 40, 4500, TRUE),
     
    ('r1000001-0000-0000-0000-000000000007', 
     'Sweet Dreams', 
     'Postres artesanales y tortas para cualquier ocasión',
     'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=800',
     'Postres',
     4.8, 178, 15, 25, 3000, FALSE),
     
    ('r1000001-0000-0000-0000-000000000008', 
     'Café Central', 
     'El mejor café colombiano con pastelería fresca',
     'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800',
     'Cafetería',
     4.6, 145, 10, 20, 2500, FALSE);

-- =============================================
-- RESTAURANT CATEGORIES (many-to-many)
-- =============================================
INSERT INTO restaurant_categories (restaurant_id, category_id) VALUES
    ('r1000001-0000-0000-0000-000000000001', 'c1000001-0000-0000-0000-000000000001'),
    ('r1000001-0000-0000-0000-000000000002', 'c1000001-0000-0000-0000-000000000002'),
    ('r1000001-0000-0000-0000-000000000003', 'c1000001-0000-0000-0000-000000000003'),
    ('r1000001-0000-0000-0000-000000000004', 'c1000001-0000-0000-0000-000000000004'),
    ('r1000001-0000-0000-0000-000000000005', 'c1000001-0000-0000-0000-000000000005'),
    ('r1000001-0000-0000-0000-000000000006', 'c1000001-0000-0000-0000-000000000008'),
    ('r1000001-0000-0000-0000-000000000007', 'c1000001-0000-0000-0000-000000000006'),
    ('r1000001-0000-0000-0000-000000000008', 'c1000001-0000-0000-0000-000000000007');

-- =============================================
-- MENU CATEGORIES
-- =============================================
-- Burger Palace
INSERT INTO menu_categories (id, restaurant_id, name, display_order) VALUES
    ('mc100001-0000-0000-0000-000000000001', 'r1000001-0000-0000-0000-000000000001', 'Hamburguesas Clásicas', 1),
    ('mc100001-0000-0000-0000-000000000002', 'r1000001-0000-0000-0000-000000000001', 'Hamburguesas Premium', 2),
    ('mc100001-0000-0000-0000-000000000003', 'r1000001-0000-0000-0000-000000000001', 'Acompañamientos', 3),
    ('mc100001-0000-0000-0000-000000000004', 'r1000001-0000-0000-0000-000000000001', 'Bebidas', 4);

-- Pizza Roma
INSERT INTO menu_categories (id, restaurant_id, name, display_order) VALUES
    ('mc200001-0000-0000-0000-000000000001', 'r1000001-0000-0000-0000-000000000002', 'Pizzas Clásicas', 1),
    ('mc200001-0000-0000-0000-000000000002', 'r1000001-0000-0000-0000-000000000002', 'Pizzas Especiales', 2),
    ('mc200001-0000-0000-0000-000000000003', 'r1000001-0000-0000-0000-000000000002', 'Entradas', 3);

-- Sushi Master
INSERT INTO menu_categories (id, restaurant_id, name, display_order) VALUES
    ('mc400001-0000-0000-0000-000000000001', 'r1000001-0000-0000-0000-000000000004', 'Rolls Clásicos', 1),
    ('mc400001-0000-0000-0000-000000000002', 'r1000001-0000-0000-0000-000000000004', 'Rolls Especiales', 2),
    ('mc400001-0000-0000-0000-000000000003', 'r1000001-0000-0000-0000-000000000004', 'Sashimi', 3);

-- Green Bowl
INSERT INTO menu_categories (id, restaurant_id, name, display_order) VALUES
    ('mc300001-0000-0000-0000-000000000001', 'r1000001-0000-0000-0000-000000000003', 'Bowls', 1),
    ('mc300001-0000-0000-0000-000000000002', 'r1000001-0000-0000-0000-000000000003', 'Ensaladas', 2),
    ('mc300001-0000-0000-0000-000000000003', 'r1000001-0000-0000-0000-000000000003', 'Smoothies', 3);

-- =============================================
-- MENU ITEMS
-- =============================================
-- Burger Palace
INSERT INTO menu_items (id, restaurant_id, category_id, name, description, price, image_url, is_popular) VALUES
    ('mi100001-0000-0000-0000-000000000001', 'r1000001-0000-0000-0000-000000000001', 'mc100001-0000-0000-0000-000000000001',
     'Hamburguesa Clásica', 'Carne 150g, lechuga, tomate, cebolla y salsa especial', 18000,
     'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400', TRUE),
     
    ('mi100001-0000-0000-0000-000000000002', 'r1000001-0000-0000-0000-000000000001', 'mc100001-0000-0000-0000-000000000001',
     'Hamburguesa con Queso', 'Carne 150g, doble queso cheddar, lechuga, tomate y salsa BBQ', 20000,
     'https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=400', TRUE),
     
    ('mi100001-0000-0000-0000-000000000003', 'r1000001-0000-0000-0000-000000000001', 'mc100001-0000-0000-0000-000000000002',
     'Hamburguesa BBQ Bacon', 'Carne 200g, bacon crujiente, aros de cebolla, queso cheddar y salsa BBQ', 28000,
     'https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?w=400', TRUE),
     
    ('mi100001-0000-0000-0000-000000000004', 'r1000001-0000-0000-0000-000000000001', 'mc100001-0000-0000-0000-000000000002',
     'Hamburguesa Doble Carne', 'Doble carne 300g, doble queso, lechuga, tomate y salsa especial', 32000,
     'https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=400', FALSE),
     
    ('mi100001-0000-0000-0000-000000000005', 'r1000001-0000-0000-0000-000000000001', 'mc100001-0000-0000-0000-000000000003',
     'Papas Fritas', 'Porción de papas fritas crujientes', 8000,
     'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400', FALSE),
     
    ('mi100001-0000-0000-0000-000000000006', 'r1000001-0000-0000-0000-000000000001', 'mc100001-0000-0000-0000-000000000003',
     'Aros de Cebolla', 'Aros de cebolla empanizados y crujientes', 10000,
     'https://images.unsplash.com/photo-1639024471283-03518883512d?w=400', FALSE);

-- Pizza Roma
INSERT INTO menu_items (id, restaurant_id, category_id, name, description, price, image_url, is_popular) VALUES
    ('mi200001-0000-0000-0000-000000000001', 'r1000001-0000-0000-0000-000000000002', 'mc200001-0000-0000-0000-000000000001',
     'Pizza Margarita', 'Salsa de tomate, mozzarella fresca y albahaca', 28000,
     'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400', TRUE),
     
    ('mi200001-0000-0000-0000-000000000002', 'r1000001-0000-0000-0000-000000000002', 'mc200001-0000-0000-0000-000000000001',
     'Pizza Pepperoni', 'Salsa de tomate, mozzarella y pepperoni', 32000,
     'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400', TRUE),
     
    ('mi200001-0000-0000-0000-000000000003', 'r1000001-0000-0000-0000-000000000002', 'mc200001-0000-0000-0000-000000000002',
     'Pizza Quattro Formaggi', 'Mozzarella, gorgonzola, parmesano y queso de cabra', 38000,
     'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400', FALSE),
     
    ('mi200001-0000-0000-0000-000000000004', 'r1000001-0000-0000-0000-000000000002', 'mc200001-0000-0000-0000-000000000002',
     'Pizza Suprema', 'Pepperoni, champiñones, pimentón, cebolla y aceitunas', 40000,
     'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400', TRUE);

-- Sushi Master
INSERT INTO menu_items (id, restaurant_id, category_id, name, description, price, image_url, is_popular) VALUES
    ('mi400001-0000-0000-0000-000000000001', 'r1000001-0000-0000-0000-000000000004', 'mc400001-0000-0000-0000-000000000001',
     'California Roll', '8 piezas con cangrejo, aguacate y pepino', 24000,
     'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=400', TRUE),
     
    ('mi400001-0000-0000-0000-000000000002', 'r1000001-0000-0000-0000-000000000004', 'mc400001-0000-0000-0000-000000000001',
     'Spicy Tuna Roll', '8 piezas con atún picante y aguacate', 28000,
     'https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56?w=400', TRUE),
     
    ('mi400001-0000-0000-0000-000000000003', 'r1000001-0000-0000-0000-000000000004', 'mc400001-0000-0000-0000-000000000002',
     'Dragon Roll', '8 piezas con tempura de camarón, aguacate y anguila', 38000,
     'https://images.unsplash.com/photo-1553621042-f6e147245754?w=400', TRUE),
     
    ('mi400001-0000-0000-0000-000000000004', 'r1000001-0000-0000-0000-000000000004', 'mc400001-0000-0000-0000-000000000003',
     'Sashimi Mixto', '12 piezas de salmón, atún y pez blanco', 45000,
     'https://images.unsplash.com/photo-1534482421-64566f976cfa?w=400', FALSE);

-- Green Bowl
INSERT INTO menu_items (id, restaurant_id, category_id, name, description, price, image_url, is_popular) VALUES
    ('mi300001-0000-0000-0000-000000000001', 'r1000001-0000-0000-0000-000000000003', 'mc300001-0000-0000-0000-000000000001',
     'Buddha Bowl', 'Quinoa, garbanzos, aguacate, zanahoria, pepino y aderezo tahini', 26000,
     'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400', TRUE),
     
    ('mi300001-0000-0000-0000-000000000002', 'r1000001-0000-0000-0000-000000000003', 'mc300001-0000-0000-0000-000000000001',
     'Poké Bowl', 'Arroz, salmón fresco, aguacate, edamame y salsa ponzu', 32000,
     'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400', TRUE),
     
    ('mi300001-0000-0000-0000-000000000003', 'r1000001-0000-0000-0000-000000000003', 'mc300001-0000-0000-0000-000000000002',
     'Ensalada César', 'Lechuga romana, pollo grillado, crutones y aderezo césar', 22000,
     'https://images.unsplash.com/photo-1550304943-4f24f54ddde9?w=400', FALSE);

-- =============================================
-- PROMO CODES
-- =============================================
INSERT INTO promo_codes (id, code, description, discount_type, discount_value, minimum_order, is_active) VALUES
    (UUID(), 'BIENVENIDO', 'Descuento de bienvenida para nuevos usuarios', 'percentage', 15, 30000, TRUE),
    (UUID(), 'ENVIOGRATIS', 'Envío gratis en tu próximo pedido', 'fixed', 5000, 25000, TRUE),
    (UUID(), 'PIZZA20', '20% de descuento en pizzas', 'percentage', 20, 40000, TRUE);
