import asyncio
import random
from uuid import uuid4
from datetime import datetime
from backend.streams.client import stream_client
from backend.streams.events import (
    ProductCreated, StockReceived, OrderCreated, OrderItemSchema, LowStockAlert
)

PRODUCTS = []

async def generate_products():
    print("Generating Products...")
    categories = ["Electronics", "Books", "Clothing", "Home"]
    
    for i in range(10):
        pid = uuid4()
        p = ProductCreated(
            product_id=pid,
            sku=f"SKU-{i:03d}",
            name=f"Demo Product {i}",
            price=random.uniform(10.0, 500.0)
        )
        await stream_client.stream.emit(p)
        PRODUCTS.append(p)
        
        # Initial Stock
        stock = StockReceived(
            product_id=pid,
            quantity=random.randint(5, 50)
        )
        await stream_client.stream.emit(stock)
        print(f"Created {p.name} with {stock.quantity} stock.")

async def simulate_orders():
    print("Simulating Orders (Ctrl+C to stop)...")
    while True:
        await asyncio.sleep(random.uniform(0.5, 2.0))
        
        if not PRODUCTS:
            continue
            
        # Create random order
        num_items = random.randint(1, 3)
        items = []
        
        for _ in range(num_items):
            prod = random.choice(PRODUCTS)
            qty = random.randint(1, 5)
            items.append(OrderItemSchema(
                product_id=prod.product_id,
                quantity=qty,
                unit_price=prod.price
            ))
            
        order = OrderCreated(
            order_id=uuid4(),
            customer_email=f"user{random.randint(1,100)}@example.com",
            items=items,
            total_amount=sum(i.quantity * i.unit_price for i in items)
        )
        
        await stream_client.stream.emit(order)
        print(f"Placed Order {order.order_id} (${order.total_amount:.2f})")
        
        # Occasional Low Stock Trigger (Manual simulation for demo)
        if random.random() < 0.1:
            prod = random.choice(PRODUCTS)
            alert = LowStockAlert(
                product_id=prod.product_id,
                current_quantity=random.randint(0, 5),
                threshold=10
            )
            await stream_client.stream.emit(alert)
            print(f"Triggered Low Stock Alert for {prod.name}")

async def main():
    await stream_client.connect()
    try:
        await generate_products()
        await simulate_orders()
    finally:
        await stream_client.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
