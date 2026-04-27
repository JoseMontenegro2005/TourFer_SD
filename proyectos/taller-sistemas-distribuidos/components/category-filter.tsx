'use client'

import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { categories } from '@/lib/data'

interface CategoryFilterProps {
  selectedCategory: string
  onSelectCategory: (category: string) => void
}

export function CategoryFilter({
  selectedCategory,
  onSelectCategory,
}: CategoryFilterProps) {
  return (
    <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
      {categories.map((category) => (
        <Button
          key={category.id}
          variant={selectedCategory === category.id ? 'default' : 'outline'}
          className={cn(
            'flex-shrink-0 gap-2 rounded-full px-4',
            selectedCategory === category.id
              ? 'bg-primary text-primary-foreground hover:bg-primary/90'
              : 'border-border bg-card text-card-foreground hover:bg-secondary hover:text-secondary-foreground'
          )}
          onClick={() => onSelectCategory(category.id)}
        >
          <span>{category.icon}</span>
          <span>{category.name}</span>
        </Button>
      ))}
    </div>
  )
}
