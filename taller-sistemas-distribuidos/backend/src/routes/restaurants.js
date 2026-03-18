import { Router } from 'express';
import { pool } from '../db.js';

const router = Router();

// Get all restaurants
router.get('/', async (req, res) => {
  try {
    const { category, featured, search, limit = 20, offset = 0 } = req.query;
    
    let query = 'SELECT * FROM restaurants WHERE is_active = TRUE';
    const params = [];

    if (category) {
      query = `
        SELECT r.* FROM restaurants r
        JOIN restaurant_categories rc ON r.id = rc.restaurant_id
        JOIN categories c ON rc.category_id = c.id
        WHERE r.is_active = TRUE AND c.name = ?
      `;
      params.push(category);
    }

    if (featured === 'true') {
      query += ' AND is_featured = TRUE';
    }

    if (search) {
      query += ' AND (name LIKE ? OR description LIKE ? OR cuisine_type LIKE ?)';
      const searchTerm = `%${search}%`;
      params.push(searchTerm, searchTerm, searchTerm);
    }

    query += ' ORDER BY rating DESC LIMIT ? OFFSET ?';
    params.push(parseInt(limit), parseInt(offset));

    const [restaurants] = await pool.query(query, params);
    res.json(restaurants);
  } catch (error) {
    console.error('Get restaurants error:', error);
    res.status(500).json({ error: 'Error al obtener restaurantes' });
  }
});

// Get featured restaurants
router.get('/featured', async (req, res) => {
  try {
    const [restaurants] = await pool.query(
      'SELECT * FROM restaurants WHERE is_active = TRUE AND is_featured = TRUE ORDER BY rating DESC LIMIT 8'
    );
    res.json(restaurants);
  } catch (error) {
    console.error('Get featured error:', error);
    res.status(500).json({ error: 'Error al obtener restaurantes destacados' });
  }
});

// Get restaurant by ID
router.get('/:id', async (req, res) => {
  try {
    const [restaurants] = await pool.query(
      'SELECT * FROM restaurants WHERE id = ? AND is_active = TRUE',
      [req.params.id]
    );

    if (restaurants.length === 0) {
      return res.status(404).json({ error: 'Restaurante no encontrado' });
    }

    const restaurant = restaurants[0];

    // Get categories
    const [categories] = await pool.query(
      `SELECT c.* FROM categories c
       JOIN restaurant_categories rc ON c.id = rc.category_id
       WHERE rc.restaurant_id = ?`,
      [req.params.id]
    );

    restaurant.categories = categories;
    res.json(restaurant);
  } catch (error) {
    console.error('Get restaurant error:', error);
    res.status(500).json({ error: 'Error al obtener restaurante' });
  }
});

// Get restaurant menu
router.get('/:id/menu', async (req, res) => {
  try {
    // Get menu categories
    const [menuCategories] = await pool.query(
      'SELECT * FROM menu_categories WHERE restaurant_id = ? ORDER BY display_order',
      [req.params.id]
    );

    // Get menu items for each category
    for (const category of menuCategories) {
      const [items] = await pool.query(
        'SELECT * FROM menu_items WHERE category_id = ? AND is_available = TRUE ORDER BY is_popular DESC, name',
        [category.id]
      );
      category.items = items;
    }

    res.json(menuCategories);
  } catch (error) {
    console.error('Get menu error:', error);
    res.status(500).json({ error: 'Error al obtener menú' });
  }
});

// Get restaurant reviews
router.get('/:id/reviews', async (req, res) => {
  try {
    const { limit = 10, offset = 0 } = req.query;
    
    const [reviews] = await pool.query(
      `SELECT r.*, u.full_name, u.avatar_url 
       FROM reviews r 
       JOIN users u ON r.user_id = u.id 
       WHERE r.restaurant_id = ? 
       ORDER BY r.created_at DESC 
       LIMIT ? OFFSET ?`,
      [req.params.id, parseInt(limit), parseInt(offset)]
    );

    res.json(reviews);
  } catch (error) {
    console.error('Get reviews error:', error);
    res.status(500).json({ error: 'Error al obtener reseñas' });
  }
});

export default router;
