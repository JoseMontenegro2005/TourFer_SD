export interface Restaurant {
  id: string
  name: string
  image: string
  rating: number
  reviewCount: number
  deliveryTime: string
  deliveryFee: string
  categories: string[]
  featured?: boolean
}

export interface MenuItem {
  id: string
  name: string
  description: string
  price: number
  image: string
  category: string
  popular?: boolean
}

export interface CartItem extends MenuItem {
  quantity: number
}

export const categories = [
  { id: 'all', name: 'All', icon: '🍽️' },
  { id: 'fast-food', name: 'Fast Food', icon: '🍔' },
  { id: 'pizza', name: 'Pizza', icon: '🍕' },
  { id: 'healthy', name: 'Healthy', icon: '🥗' },
  { id: 'asian', name: 'Asian', icon: '🍜' },
  { id: 'mexican', name: 'Mexican', icon: '🌮' },
  { id: 'desserts', name: 'Desserts', icon: '🍰' },
  { id: 'coffee', name: 'Coffee', icon: '☕' },
]

export const restaurants: Restaurant[] = [
  {
    id: '1',
    name: 'Burger Palace',
    image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&h=300&fit=crop',
    rating: 4.8,
    reviewCount: 243,
    deliveryTime: '15-25 min',
    deliveryFee: '$2.99',
    categories: ['fast-food'],
    featured: true,
  },
  {
    id: '2',
    name: 'Pizza Heaven',
    image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=500&h=300&fit=crop',
    rating: 4.6,
    reviewCount: 189,
    deliveryTime: '20-30 min',
    deliveryFee: '$1.99',
    categories: ['pizza'],
    featured: true,
  },
  {
    id: '3',
    name: 'Green Garden',
    image: 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=500&h=300&fit=crop',
    rating: 4.9,
    reviewCount: 156,
    deliveryTime: '15-20 min',
    deliveryFee: 'Free',
    categories: ['healthy'],
  },
  {
    id: '4',
    name: 'Tokyo Ramen',
    image: 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500&h=300&fit=crop',
    rating: 4.7,
    reviewCount: 312,
    deliveryTime: '25-35 min',
    deliveryFee: '$3.49',
    categories: ['asian'],
  },
  {
    id: '5',
    name: 'Taco Fiesta',
    image: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=500&h=300&fit=crop',
    rating: 4.5,
    reviewCount: 198,
    deliveryTime: '20-30 min',
    deliveryFee: '$2.49',
    categories: ['mexican'],
  },
  {
    id: '6',
    name: 'Sweet Delights',
    image: 'https://images.unsplash.com/photo-1551024601-bec78aea704b?w=500&h=300&fit=crop',
    rating: 4.8,
    reviewCount: 267,
    deliveryTime: '15-25 min',
    deliveryFee: '$1.49',
    categories: ['desserts'],
  },
  {
    id: '7',
    name: 'Brew & Beans',
    image: 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=500&h=300&fit=crop',
    rating: 4.6,
    reviewCount: 145,
    deliveryTime: '10-20 min',
    deliveryFee: 'Free',
    categories: ['coffee'],
  },
  {
    id: '8',
    name: 'Crispy Chicken',
    image: 'https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=500&h=300&fit=crop',
    rating: 4.4,
    reviewCount: 223,
    deliveryTime: '20-30 min',
    deliveryFee: '$2.99',
    categories: ['fast-food'],
  },
]

export const menuItems: Record<string, MenuItem[]> = {
  '1': [
    {
      id: '1-1',
      name: 'Classic Cheeseburger',
      description: 'Juicy beef patty with melted cheddar, lettuce, tomato, and our special sauce',
      price: 12.99,
      image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&h=200&fit=crop',
      category: 'Burgers',
      popular: true,
    },
    {
      id: '1-2',
      name: 'Double Stack Burger',
      description: 'Two beef patties, double cheese, bacon, pickles, and onions',
      price: 16.99,
      image: 'https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=300&h=200&fit=crop',
      category: 'Burgers',
      popular: true,
    },
    {
      id: '1-3',
      name: 'Crispy Fries',
      description: 'Golden crispy fries with sea salt',
      price: 4.99,
      image: 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=300&h=200&fit=crop',
      category: 'Sides',
    },
    {
      id: '1-4',
      name: 'Onion Rings',
      description: 'Crispy battered onion rings with dipping sauce',
      price: 5.99,
      image: 'https://images.unsplash.com/photo-1639024471283-03518883512d?w=300&h=200&fit=crop',
      category: 'Sides',
    },
    {
      id: '1-5',
      name: 'Chocolate Milkshake',
      description: 'Creamy chocolate milkshake topped with whipped cream',
      price: 6.99,
      image: 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=300&h=200&fit=crop',
      category: 'Drinks',
    },
    {
      id: '1-6',
      name: 'Veggie Burger',
      description: 'Plant-based patty with avocado, lettuce, and vegan mayo',
      price: 13.99,
      image: 'https://images.unsplash.com/photo-1520072959219-c595dc870360?w=300&h=200&fit=crop',
      category: 'Burgers',
    },
  ],
  '2': [
    {
      id: '2-1',
      name: 'Margherita Pizza',
      description: 'Fresh mozzarella, tomatoes, and basil on our signature crust',
      price: 14.99,
      image: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=300&h=200&fit=crop',
      category: 'Pizzas',
      popular: true,
    },
    {
      id: '2-2',
      name: 'Pepperoni Feast',
      description: 'Loaded with premium pepperoni and extra cheese',
      price: 16.99,
      image: 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=300&h=200&fit=crop',
      category: 'Pizzas',
      popular: true,
    },
    {
      id: '2-3',
      name: 'BBQ Chicken Pizza',
      description: 'Grilled chicken, BBQ sauce, red onions, and cilantro',
      price: 17.99,
      image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=300&h=200&fit=crop',
      category: 'Pizzas',
    },
    {
      id: '2-4',
      name: 'Garlic Bread',
      description: 'Toasted bread with garlic butter and herbs',
      price: 5.99,
      image: 'https://images.unsplash.com/photo-1619535860434-ba1d8fa12536?w=300&h=200&fit=crop',
      category: 'Sides',
    },
    {
      id: '2-5',
      name: 'Caesar Salad',
      description: 'Crisp romaine, parmesan, croutons, and Caesar dressing',
      price: 8.99,
      image: 'https://images.unsplash.com/photo-1550304943-4f24f54ddde9?w=300&h=200&fit=crop',
      category: 'Salads',
    },
  ],
  '3': [
    {
      id: '3-1',
      name: 'Buddha Bowl',
      description: 'Quinoa, roasted vegetables, chickpeas, and tahini dressing',
      price: 13.99,
      image: 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=300&h=200&fit=crop',
      category: 'Bowls',
      popular: true,
    },
    {
      id: '3-2',
      name: 'Acai Bowl',
      description: 'Acai blend topped with granola, berries, and honey',
      price: 11.99,
      image: 'https://images.unsplash.com/photo-1590301157890-4810ed352733?w=300&h=200&fit=crop',
      category: 'Bowls',
      popular: true,
    },
    {
      id: '3-3',
      name: 'Green Smoothie',
      description: 'Spinach, banana, mango, and almond milk',
      price: 7.99,
      image: 'https://images.unsplash.com/photo-1610970881699-44a5587cabec?w=300&h=200&fit=crop',
      category: 'Drinks',
    },
    {
      id: '3-4',
      name: 'Avocado Toast',
      description: 'Sourdough with smashed avocado, cherry tomatoes, and microgreens',
      price: 10.99,
      image: 'https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=300&h=200&fit=crop',
      category: 'Toasts',
    },
  ],
  '4': [
    {
      id: '4-1',
      name: 'Tonkotsu Ramen',
      description: 'Rich pork bone broth with chashu, soft egg, and nori',
      price: 15.99,
      image: 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=300&h=200&fit=crop',
      category: 'Ramen',
      popular: true,
    },
    {
      id: '4-2',
      name: 'Miso Ramen',
      description: 'Savory miso broth with corn, butter, and bean sprouts',
      price: 14.99,
      image: 'https://images.unsplash.com/photo-1557872943-16a5ac26437e?w=300&h=200&fit=crop',
      category: 'Ramen',
    },
    {
      id: '4-3',
      name: 'Gyoza (6 pcs)',
      description: 'Pan-fried pork dumplings with dipping sauce',
      price: 8.99,
      image: 'https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=300&h=200&fit=crop',
      category: 'Appetizers',
      popular: true,
    },
    {
      id: '4-4',
      name: 'Edamame',
      description: 'Steamed soybeans with sea salt',
      price: 5.99,
      image: 'https://images.unsplash.com/photo-1564894809611-1742fc40ed80?w=300&h=200&fit=crop',
      category: 'Appetizers',
    },
  ],
  '5': [
    {
      id: '5-1',
      name: 'Carne Asada Tacos',
      description: 'Grilled steak with onions, cilantro, and salsa verde',
      price: 12.99,
      image: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=300&h=200&fit=crop',
      category: 'Tacos',
      popular: true,
    },
    {
      id: '5-2',
      name: 'Chicken Burrito',
      description: 'Flour tortilla filled with chicken, rice, beans, and cheese',
      price: 11.99,
      image: 'https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=300&h=200&fit=crop',
      category: 'Burritos',
      popular: true,
    },
    {
      id: '5-3',
      name: 'Guacamole & Chips',
      description: 'Fresh guacamole with house-made tortilla chips',
      price: 8.99,
      image: 'https://images.unsplash.com/photo-1615870216519-2f9fa575fa5c?w=300&h=200&fit=crop',
      category: 'Appetizers',
    },
    {
      id: '5-4',
      name: 'Churros',
      description: 'Cinnamon sugar churros with chocolate sauce',
      price: 6.99,
      image: 'https://images.unsplash.com/photo-1624371414361-e670b70b8e5b?w=300&h=200&fit=crop',
      category: 'Desserts',
    },
  ],
  '6': [
    {
      id: '6-1',
      name: 'Chocolate Lava Cake',
      description: 'Warm chocolate cake with molten center and vanilla ice cream',
      price: 9.99,
      image: 'https://images.unsplash.com/photo-1551024601-bec78aea704b?w=300&h=200&fit=crop',
      category: 'Cakes',
      popular: true,
    },
    {
      id: '6-2',
      name: 'New York Cheesecake',
      description: 'Creamy cheesecake with graham cracker crust',
      price: 8.99,
      image: 'https://images.unsplash.com/photo-1524351199678-941a58a3df50?w=300&h=200&fit=crop',
      category: 'Cakes',
      popular: true,
    },
    {
      id: '6-3',
      name: 'Tiramisu',
      description: 'Classic Italian dessert with espresso-soaked ladyfingers',
      price: 8.99,
      image: 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=300&h=200&fit=crop',
      category: 'Desserts',
    },
    {
      id: '6-4',
      name: 'Ice Cream Sundae',
      description: 'Three scoops with hot fudge, whipped cream, and cherry',
      price: 7.99,
      image: 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=300&h=200&fit=crop',
      category: 'Ice Cream',
    },
  ],
  '7': [
    {
      id: '7-1',
      name: 'Cappuccino',
      description: 'Espresso with steamed milk and foam',
      price: 4.99,
      image: 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=300&h=200&fit=crop',
      category: 'Coffee',
      popular: true,
    },
    {
      id: '7-2',
      name: 'Iced Latte',
      description: 'Espresso with cold milk over ice',
      price: 5.49,
      image: 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=300&h=200&fit=crop',
      category: 'Coffee',
      popular: true,
    },
    {
      id: '7-3',
      name: 'Croissant',
      description: 'Buttery, flaky French pastry',
      price: 3.99,
      image: 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=300&h=200&fit=crop',
      category: 'Pastries',
    },
    {
      id: '7-4',
      name: 'Blueberry Muffin',
      description: 'Fresh-baked muffin loaded with blueberries',
      price: 3.49,
      image: 'https://images.unsplash.com/photo-1607958996333-41aef7caefaa?w=300&h=200&fit=crop',
      category: 'Pastries',
    },
  ],
  '8': [
    {
      id: '8-1',
      name: 'Crispy Chicken Sandwich',
      description: 'Crispy fried chicken breast with pickles and spicy mayo',
      price: 11.99,
      image: 'https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=300&h=200&fit=crop',
      category: 'Sandwiches',
      popular: true,
    },
    {
      id: '8-2',
      name: 'Chicken Tenders',
      description: '5 crispy chicken tenders with your choice of sauce',
      price: 10.99,
      image: 'https://images.unsplash.com/photo-1562967914-608f82629710?w=300&h=200&fit=crop',
      category: 'Chicken',
      popular: true,
    },
    {
      id: '8-3',
      name: 'Chicken Wings (8 pcs)',
      description: 'Crispy wings tossed in buffalo or BBQ sauce',
      price: 12.99,
      image: 'https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=300&h=200&fit=crop',
      category: 'Chicken',
    },
    {
      id: '8-4',
      name: 'Coleslaw',
      description: 'Creamy homemade coleslaw',
      price: 3.99,
      image: 'https://images.unsplash.com/photo-1625938145744-e380515399bf?w=300&h=200&fit=crop',
      category: 'Sides',
    },
  ],
}

export function getRestaurantById(id: string): Restaurant | undefined {
  return restaurants.find((r) => r.id === id)
}

export function getMenuByRestaurantId(id: string): MenuItem[] {
  return menuItems[id] || []
}
