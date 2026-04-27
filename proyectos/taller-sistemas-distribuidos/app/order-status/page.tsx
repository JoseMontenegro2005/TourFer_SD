'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { CheckCircle2, Clock, ChefHat, Bike, Home, Package } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { cn } from '@/lib/utils'

type OrderStatus = 'confirmed' | 'preparing' | 'on-the-way' | 'delivered'

interface StatusStep {
  id: OrderStatus
  label: string
  description: string
  icon: React.ComponentType<{ className?: string }>
}

const statusSteps: StatusStep[] = [
  {
    id: 'confirmed',
    label: 'Order Confirmed',
    description: 'Your order has been received',
    icon: CheckCircle2,
  },
  {
    id: 'preparing',
    label: 'Preparing',
    description: 'The restaurant is preparing your food',
    icon: ChefHat,
  },
  {
    id: 'on-the-way',
    label: 'On the Way',
    description: 'Your order is out for delivery',
    icon: Bike,
  },
  {
    id: 'delivered',
    label: 'Delivered',
    description: 'Your order has been delivered',
    icon: Home,
  },
]

export default function OrderStatusPage() {
  const [currentStatus, setCurrentStatus] = useState<OrderStatus>('confirmed')
  const [progress, setProgress] = useState(0)

  // Simulate order progress
  useEffect(() => {
    const statusOrder: OrderStatus[] = ['confirmed', 'preparing', 'on-the-way', 'delivered']
    let currentIndex = 0

    const interval = setInterval(() => {
      if (currentIndex < statusOrder.length - 1) {
        currentIndex++
        setCurrentStatus(statusOrder[currentIndex])
        setProgress((currentIndex / (statusOrder.length - 1)) * 100)
      } else {
        clearInterval(interval)
      }
    }, 5000) // Update every 5 seconds for demo

    return () => clearInterval(interval)
  }, [])

  const getCurrentStatusIndex = () => {
    return statusSteps.findIndex((step) => step.id === currentStatus)
  }

  const orderId = 'FD-' + Math.random().toString(36).substring(2, 8).toUpperCase()
  const estimatedTime = currentStatus === 'delivered' ? 'Delivered' : '20-30 min'

  return (
    <div className="min-h-screen bg-background">
      <div className="mx-auto max-w-3xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
            <Package className="h-8 w-8 text-primary" />
          </div>
          <h1 className="text-3xl font-bold text-foreground">Order Placed!</h1>
          <p className="mt-2 text-muted-foreground">
            Order #{orderId}
          </p>
        </div>

        {/* Progress Card */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Order Status</span>
              <span className="flex items-center gap-2 text-sm font-normal text-muted-foreground">
                <Clock className="h-4 w-4" />
                {estimatedTime}
              </span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Progress value={progress} className="mb-8 h-2" />

            <div className="relative">
              {statusSteps.map((step, index) => {
                const StatusIcon = step.icon
                const isCompleted = index <= getCurrentStatusIndex()
                const isCurrent = index === getCurrentStatusIndex()

                return (
                  <div
                    key={step.id}
                    className={cn(
                      'relative flex gap-4 pb-8 last:pb-0',
                      index < statusSteps.length - 1 &&
                        "before:absolute before:left-5 before:top-10 before:h-full before:w-0.5 before:content-['']",
                      isCompleted
                        ? 'before:bg-primary'
                        : 'before:bg-border'
                    )}
                  >
                    <div
                      className={cn(
                        'relative z-10 flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full transition-colors',
                        isCompleted
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-muted text-muted-foreground'
                      )}
                    >
                      <StatusIcon className="h-5 w-5" />
                      {isCurrent && (
                        <span className="absolute -inset-1 animate-ping rounded-full bg-primary/30" />
                      )}
                    </div>
                    <div className="flex-1 pt-1">
                      <h3
                        className={cn(
                          'font-semibold',
                          isCompleted ? 'text-foreground' : 'text-muted-foreground'
                        )}
                      >
                        {step.label}
                      </h3>
                      <p className="text-sm text-muted-foreground">
                        {step.description}
                      </p>
                    </div>
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>

        {/* Delivery Details */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Delivery Details</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="text-sm text-muted-foreground">Delivering to</p>
              <p className="font-medium text-foreground">123 Main Street, New York, NY 10001</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Contact</p>
              <p className="font-medium text-foreground">(555) 123-4567</p>
            </div>
          </CardContent>
        </Card>

        {/* Actions */}
        <div className="flex flex-col gap-4 sm:flex-row">
          <Link href="/" className="flex-1">
            <Button variant="outline" className="w-full">
              Order Again
            </Button>
          </Link>
          <Button className="flex-1" disabled={currentStatus === 'delivered'}>
            {currentStatus === 'delivered' ? 'Order Complete' : 'Track Driver'}
          </Button>
        </div>

        {/* Support */}
        <p className="mt-8 text-center text-sm text-muted-foreground">
          Need help?{' '}
          <button className="text-primary hover:underline">Contact Support</button>
        </p>
      </div>
    </div>
  )
}
