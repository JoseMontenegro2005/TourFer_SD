'use client'

import Image from 'next/image'
import { Plus } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { useCart } from '@/lib/cart-context'
import type { MenuItem } from '@/lib/data'

interface MenuItemCardProps {
  item: MenuItem
}

export function MenuItemCard({ item }: MenuItemCardProps) {
  const { addItem, setIsOpen } = useCart()

  const handleAddToCart = () => {
    addItem(item)
    setIsOpen(true)
  }

  return (
    <Card className="group overflow-hidden transition-all duration-300 hover:shadow-md">
      <div className="flex gap-4 p-4">
        <div className="flex-1">
          <div className="flex items-start gap-2">
            <h3 className="font-semibold text-foreground">{item.name}</h3>
            {item.popular && (
              <Badge variant="secondary" className="bg-primary/10 text-primary">
                Popular
              </Badge>
            )}
          </div>
          <p className="mt-1 line-clamp-2 text-sm text-muted-foreground">
            {item.description}
          </p>
          <p className="mt-3 text-lg font-semibold text-primary">
            ${item.price.toFixed(2)}
          </p>
        </div>
        <div className="relative">
          <div className="relative h-24 w-24 overflow-hidden rounded-lg">
            <Image
              src={item.image}
              alt={item.name}
              fill
              className="object-cover"
            />
          </div>
          <Button
            size="icon"
            className="absolute -bottom-2 -right-2 h-8 w-8 rounded-full shadow-md"
            onClick={handleAddToCart}
          >
            <Plus className="h-4 w-4" />
            <span className="sr-only">Add {item.name} to cart</span>
          </Button>
        </div>
      </div>
    </Card>
  )
}
