import { Router } from 'express';
import { pool } from '../db.js';

const router = Router();

// Get menu item by ID
router.get('/items/:id', async (req, res) => {
  try {
    const [items] = await pool.query(
      'SELECT * FROM menu_items WHERE id = ?',
      [req.params.id]
    );

    if (items.length === 0) {
      return res.status(404).json({ error: 'Item no encontrado' });
    }

    const item = items[0];

    // Get item options
    const [options] = await pool.query(
      'SELECT * FROM menu_item_options WHERE menu_item_id = ?',
      [req.params.id]
    );

    for (const option of options) {
      const [values] = await pool.query(
        'SELECT * FROM menu_item_option_values WHERE option_id = ?',
        [option.id]
      );
      option.values = values;
    }

    item.options = options;
    res.json(item);
  } catch (error) {
    console.error('Get menu item error:', error);
    res.status(500).json({ error: 'Error al obtener item del menú' });
  }
});

// Search menu items
router.get('/search', async (req, res) => {
  try {
    const { q, restaurantId, limit = 20 } = req.query;

    if (!q) {
      return res.status(400).json({ error: 'Se requiere término de búsqueda' });
    }

    let query = `
      SELECT mi.*, r.name as restaurant_name 
      FROM menu_items mi 
      JOIN restaurants r ON mi.restaurant_id = r.id 
      WHERE mi.is_available = TRUE 
      AND (mi.name LIKE ? OR mi.description LIKE ?)
    `;
    const params = [`%${q}%`, `%${q}%`];

    if (restaurantId) {
      query += ' AND mi.restaurant_id = ?';
      params.push(restaurantId);
    }

    query += ' ORDER BY mi.is_popular DESC LIMIT ?';
    params.push(parseInt(limit));

    const [items] = await pool.query(query, params);
    res.json(items);
  } catch (error) {
    console.error('Search menu error:', error);
    res.status(500).json({ error: 'Error al buscar en el menú' });
  }
});

export default router;
