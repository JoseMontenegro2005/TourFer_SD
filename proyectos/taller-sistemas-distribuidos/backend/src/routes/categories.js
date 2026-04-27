import { Router } from 'express';
import { pool } from '../db.js';

const router = Router();

// Get all categories
router.get('/', async (req, res) => {
  try {
    const [categories] = await pool.query(
      'SELECT * FROM categories ORDER BY display_order'
    );
    res.json(categories);
  } catch (error) {
    console.error('Get categories error:', error);
    res.status(500).json({ error: 'Error al obtener categorías' });
  }
});

// Get category by ID
router.get('/:id', async (req, res) => {
  try {
    const [categories] = await pool.query(
      'SELECT * FROM categories WHERE id = ?',
      [req.params.id]
    );

    if (categories.length === 0) {
      return res.status(404).json({ error: 'Categoría no encontrada' });
    }

    res.json(categories[0]);
  } catch (error) {
    console.error('Get category error:', error);
    res.status(500).json({ error: 'Error al obtener categoría' });
  }
});

// Get restaurants by category
router.get('/:id/restaurants', async (req, res) => {
  try {
    const { limit = 20, offset = 0 } = req.query;

    const [restaurants] = await pool.query(
      `SELECT r.* FROM restaurants r
       JOIN restaurant_categories rc ON r.id = rc.restaurant_id
       WHERE rc.category_id = ? AND r.is_active = TRUE
       ORDER BY r.rating DESC
       LIMIT ? OFFSET ?`,
      [req.params.id, parseInt(limit), parseInt(offset)]
    );

    res.json(restaurants);
  } catch (error) {
    console.error('Get restaurants by category error:', error);
    res.status(500).json({ error: 'Error al obtener restaurantes' });
  }
});

export default router;
