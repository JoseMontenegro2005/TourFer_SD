import Image from 'next/image'
import Link from 'next/link'
import { Star, Clock } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import type { Restaurant } from '@/lib/data'

interface RestaurantCardProps {
  restaurant: Restaurant
  priority?: boolean
}

export function RestaurantCard({ restaurant, priority = false }: RestaurantCardProps) {
  return (
    <Link href={`/restaurant/${restaurant.id}`}>
      <Card className="group overflow-hidden transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
        <div className="relative aspect-[16/10] overflow-hidden">
          <Image
            src={restaurant.image}
            alt={restaurant.name}
            fill
            priority={priority}
            className="object-cover transition-transform duration-300 group-hover:scale-105"
          />
          {restaurant.featured && (
            <Badge className="absolute left-3 top-3 bg-primary text-primary-foreground">
              Featured
            </Badge>
          )}
          {restaurant.deliveryFee === 'Free' && (
            <Badge
              variant="secondary"
              className="absolute right-3 top-3 bg-background/90 text-foreground"
            >
              Free Delivery
            </Badge>
          )}
        </div>
        <CardContent className="p-4">
          <h3 className="font-semibold text-foreground group-hover:text-primary transition-colors">
            {restaurant.name}
          </h3>
          <div className="mt-2 flex items-center gap-4 text-sm">
            <div className="flex items-center gap-1">
              <Star className="h-4 w-4 fill-primary text-primary" />
              <span className="font-medium text-foreground">{restaurant.rating}</span>
              <span className="text-muted-foreground">({restaurant.reviewCount})</span>
            </div>
            <div className="flex items-center gap-1 text-muted-foreground">
              <Clock className="h-4 w-4" />
              <span>{restaurant.deliveryTime}</span>
            </div>
          </div>
          <p className="mt-2 text-sm text-muted-foreground">
            Delivery {restaurant.deliveryFee}
          </p>
        </CardContent>
      </Card>
    </Link>
  )
}
