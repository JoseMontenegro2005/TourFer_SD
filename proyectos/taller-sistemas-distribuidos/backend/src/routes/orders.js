import { Router } from 'express';
import { v4 as uuidv4 } from 'uuid';
import { pool } from '../db.js';
import { authenticateToken } from '../middleware/auth.js';

const router = Router();

// Create order
router.post('/', authenticateToken, async (req, res) => {
  const connection = await pool.getConnection();
  
  try {
    await connection.beginTransaction();

    const {
      restaurantId,
      items,
      deliveryAddress,
      deliveryInstructions,
      paymentMethod,
      promoCode
    } = req.body;

    // Calculate totals
    let subtotal = 0;
    for (const item of items) {
      const [menuItems] = await connection.query(
        'SELECT price FROM menu_items WHERE id = ?',
        [item.menuItemId]
      );
      if (menuItems.length === 0) {
        throw new Error(`Item ${item.menuItemId} no encontrado`);
      }
      subtotal += menuItems[0].price * item.quantity;
    }

    // Get delivery fee
    const [restaurants] = await connection.query(
      'SELECT delivery_fee FROM restaurants WHERE id = ?',
      [restaurantId]
    );
    const deliveryFee = restaurants[0]?.delivery_fee || 0;

    // Apply promo code if provided
    let discount = 0;
    if (promoCode) {
      const [promos] = await connection.query(
        'SELECT * FROM promo_codes WHERE code = ? AND is_active = TRUE',
        [promoCode]
      );
      if (promos.length > 0) {
        const promo = promos[0];
        if (subtotal >= promo.minimum_order) {
          if (promo.discount_type === 'percentage') {
            discount = (subtotal * promo.discount_value) / 100;
          } else {
            discount = promo.discount_value;
          }
          // Update promo usage
          await connection.query(
            'UPDATE promo_codes SET current_uses = current_uses + 1 WHERE id = ?',
            [promo.id]
          );
        }
      }
    }

    const serviceFee = subtotal * 0.05; // 5% service fee
    const total = subtotal + deliveryFee + serviceFee - discount;

    // Create order
    const orderId = uuidv4();
    const estimatedDelivery = new Date(Date.now() + 45 * 60 * 1000); // 45 minutes

    await connection.query(
      `INSERT INTO orders (id, user_id, restaurant_id, delivery_address, delivery_instructions,
        subtotal, delivery_fee, service_fee, discount, total, payment_method, estimated_delivery_time)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      [orderId, req.user.id, restaurantId, deliveryAddress, deliveryInstructions || null,
       subtotal, deliveryFee, serviceFee, discount, total, paymentMethod, estimatedDelivery]
    );

    // Add order items
    for (const item of items) {
      const [menuItems] = await connection.query(
        'SELECT price FROM menu_items WHERE id = ?',
        [item.menuItemId]
      );
      const unitPrice = menuItems[0].price;
      const totalPrice = unitPrice * item.quantity;

      await connection.query(
        `INSERT INTO order_items (id, order_id, menu_item_id, quantity, unit_price, total_price, special_instructions, options_json)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
        [uuidv4(), orderId, item.menuItemId, item.quantity, unitPrice, totalPrice, 
         item.specialInstructions || null, item.options ? JSON.stringify(item.options) : null]
      );
    }

    // Add initial status history
    await connection.query(
      'INSERT INTO order_status_history (id, order_id, status, notes) VALUES (?, ?, ?, ?)',
      [uuidv4(), orderId, 'pending', 'Pedido creado']
    );

    await connection.commit();

    // Get full order details
    const [orders] = await pool.query(
      'SELECT * FROM orders WHERE id = ?',
      [orderId]
    );

    res.status(201).json({
      message: 'Pedido creado exitosamente',
      order: orders[0]
    });
  } catch (error) {
    await connection.rollback();
    console.error('Create order error:', error);
    res.status(500).json({ error: 'Error al crear pedido' });
  } finally {
    connection.release();
  }
});

// Get user orders
router.get('/', authenticateToken, async (req, res) => {
  try {
    const { status, limit = 10, offset = 0 } = req.query;

    let query = `
      SELECT o.*, r.name as restaurant_name, r.image_url as restaurant_image
      FROM orders o
      JOIN restaurants r ON o.restaurant_id = r.id
      WHERE o.user_id = ?
    `;
    const params = [req.user.id];

    if (status) {
      query += ' AND o.status = ?';
      params.push(status);
    }

    query += ' ORDER BY o.created_at DESC LIMIT ? OFFSET ?';
    params.push(parseInt(limit), parseInt(offset));

    const [orders] = await pool.query(query, params);
    res.json(orders);
  } catch (error) {
    console.error('Get orders error:', error);
    res.status(500).json({ error: 'Error al obtener pedidos' });
  }
});

// Get order by ID
router.get('/:id', authenticateToken, async (req, res) => {
  try {
    const [orders] = await pool.query(
      `SELECT o.*, r.name as restaurant_name, r.image_url as restaurant_image, r.phone as restaurant_phone
       FROM orders o
       JOIN restaurants r ON o.restaurant_id = r.id
       WHERE o.id = ? AND o.user_id = ?`,
      [req.params.id, req.user.id]
    );

    if (orders.length === 0) {
      return res.status(404).json({ error: 'Pedido no encontrado' });
    }

    const order = orders[0];

    // Get order items
    const [items] = await pool.query(
      `SELECT oi.*, mi.name, mi.image_url
       FROM order_items oi
       JOIN menu_items mi ON oi.menu_item_id = mi.id
       WHERE oi.order_id = ?`,
      [req.params.id]
    );
    order.items = items;

    // Get status history
    const [history] = await pool.query(
      'SELECT * FROM order_status_history WHERE order_id = ? ORDER BY created_at DESC',
      [req.params.id]
    );
    order.statusHistory = history;

    res.json(order);
  } catch (error) {
    console.error('Get order error:', error);
    res.status(500).json({ error: 'Error al obtener pedido' });
  }
});

// Update order status (for testing/admin)
router.patch('/:id/status', authenticateToken, async (req, res) => {
  try {
    const { status, notes } = req.body;
    const validStatuses = ['pending', 'confirmed', 'preparing', 'ready', 'on_the_way', 'delivered', 'cancelled'];

    if (!validStatuses.includes(status)) {
      return res.status(400).json({ error: 'Estado inválido' });
    }

    await pool.query(
      'UPDATE orders SET status = ? WHERE id = ?',
      [status, req.params.id]
    );

    await pool.query(
      'INSERT INTO order_status_history (id, order_id, status, notes) VALUES (?, ?, ?, ?)',
      [uuidv4(), req.params.id, status, notes || null]
    );

    res.json({ message: 'Estado actualizado' });
  } catch (error) {
    console.error('Update status error:', error);
    res.status(500).json({ error: 'Error al actualizar estado' });
  }
});

export default router;
