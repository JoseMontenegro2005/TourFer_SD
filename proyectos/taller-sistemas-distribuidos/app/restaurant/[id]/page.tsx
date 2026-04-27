import Image from 'next/image'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { Star, Clock, ChevronLeft, MapPin } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { MenuItemCard } from '@/components/menu-item'
import { getRestaurantById, getMenuByRestaurantId } from '@/lib/data'

interface RestaurantPageProps {
  params: Promise<{ id: string }>
}

export default async function RestaurantPage({ params }: RestaurantPageProps) {
  const { id } = await params
  const restaurant = getRestaurantById(id)
  const menuItems = getMenuByRestaurantId(id)

  if (!restaurant) {
    notFound()
  }

  // Group menu items by category
  const menuByCategory = menuItems.reduce(
    (acc, item) => {
      if (!acc[item.category]) {
        acc[item.category] = []
      }
      acc[item.category].push(item)
      return acc
    },
    {} as Record<string, typeof menuItems>
  )

  const categories = Object.keys(menuByCategory)

  return (
    <div className="min-h-screen bg-background">
      {/* Restaurant Header */}
      <div className="relative h-64 sm:h-80">
        <Image
          src={restaurant.image}
          alt={restaurant.name}
          fill
          className="object-cover"
          priority
        />
        <div className="absolute inset-0 bg-gradient-to-t from-background/90 via-background/50 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 px-4 pb-6 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-7xl">
            <Link href="/">
              <Button variant="secondary" size="sm" className="mb-4">
                <ChevronLeft className="mr-1 h-4 w-4" />
                Back to restaurants
              </Button>
            </Link>
            <h1 className="text-3xl font-bold text-foreground sm:text-4xl">
              {restaurant.name}
            </h1>
            <div className="mt-3 flex flex-wrap items-center gap-4 text-sm">
              <div className="flex items-center gap-1">
                <Star className="h-5 w-5 fill-primary text-primary" />
                <span className="font-semibold text-foreground">{restaurant.rating}</span>
                <span className="text-muted-foreground">
                  ({restaurant.reviewCount} reviews)
                </span>
              </div>
              <div className="flex items-center gap-1 text-muted-foreground">
                <Clock className="h-4 w-4" />
                <span>{restaurant.deliveryTime}</span>
              </div>
              <div className="flex items-center gap-1 text-muted-foreground">
                <MapPin className="h-4 w-4" />
                <span>0.5 miles away</span>
              </div>
              <Badge variant="secondary" className="bg-primary/10 text-primary">
                Delivery {restaurant.deliveryFee}
              </Badge>
            </div>
          </div>
        </div>
      </div>

      {/* Menu */}
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Category Navigation */}
        <div className="mb-8 flex gap-2 overflow-x-auto pb-2">
          {categories.map((category) => (
            <a
              key={category}
              href={`#${category.toLowerCase().replace(/\s+/g, '-')}`}
              className="flex-shrink-0 rounded-full border border-border bg-card px-4 py-2 text-sm font-medium text-card-foreground transition-colors hover:bg-primary hover:text-primary-foreground"
            >
              {category}
            </a>
          ))}
        </div>

        {/* Menu Sections */}
        <div className="space-y-10">
          {categories.map((category) => (
            <section
              key={category}
              id={category.toLowerCase().replace(/\s+/g, '-')}
              className="scroll-mt-20"
            >
              <h2 className="mb-6 text-2xl font-bold text-foreground">{category}</h2>
              <div className="grid gap-4 sm:grid-cols-2">
                {menuByCategory[category].map((item) => (
                  <MenuItemCard key={item.id} item={item} />
                ))}
              </div>
            </section>
          ))}
        </div>
      </div>
    </div>
  )
}
