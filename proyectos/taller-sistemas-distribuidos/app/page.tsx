'use client'

import { useState } from 'react'
import { RestaurantCard } from '@/components/restaurant-card'
import { CategoryFilter } from '@/components/category-filter'
import { restaurants } from '@/lib/data'

export default function HomePage() {
  const [selectedCategory, setSelectedCategory] = useState('all')

  const filteredRestaurants =
    selectedCategory === 'all'
      ? restaurants
      : restaurants.filter((r) => r.categories.includes(selectedCategory))

  const featuredRestaurants = restaurants.filter((r) => r.featured)

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary/10 via-primary/5 to-background px-4 py-12 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <h1 className="text-balance text-4xl font-bold tracking-tight text-foreground sm:text-5xl">
            Delicious food,{' '}
            <span className="text-primary">delivered fast</span>
          </h1>
          <p className="mt-4 max-w-2xl text-lg text-muted-foreground">
            Order from the best local restaurants with easy, contactless delivery.
          </p>
        </div>
      </section>

      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Category Filter */}
        <section className="mb-8">
          <h2 className="mb-4 text-lg font-semibold text-foreground">Categories</h2>
          <CategoryFilter
            selectedCategory={selectedCategory}
            onSelectCategory={setSelectedCategory}
          />
        </section>

        {/* Featured Restaurants */}
        {selectedCategory === 'all' && featuredRestaurants.length > 0 && (
          <section className="mb-12">
            <h2 className="mb-6 text-2xl font-bold text-foreground">Featured Restaurants</h2>
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {featuredRestaurants.map((restaurant, index) => (
                <RestaurantCard key={restaurant.id} restaurant={restaurant} priority={index < 3} />
              ))}
            </div>
          </section>
        )}

        {/* All Restaurants */}
        <section>
          <h2 className="mb-6 text-2xl font-bold text-foreground">
            {selectedCategory === 'all' ? 'All Restaurants' : 'Results'}
          </h2>
          {filteredRestaurants.length > 0 ? (
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {filteredRestaurants.map((restaurant) => (
                <RestaurantCard key={restaurant.id} restaurant={restaurant} />
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-16 text-center">
              <p className="text-lg font-medium text-muted-foreground">
                No restaurants found in this category
              </p>
              <button
                onClick={() => setSelectedCategory('all')}
                className="mt-4 text-primary hover:underline"
              >
                View all restaurants
              </button>
            </div>
          )}
        </section>
      </div>
    </div>
  )
}
