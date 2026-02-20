import asyncio
import httpx
import random
import logging
import os
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Simulator")

API_URL = os.getenv("API_URL", "http://backend-api:8000")
SIM_PROFILE = os.getenv("SIM_PROFILE", "NORMAL")

DEMO_PRODUCTS = [
    {"sku": "LAP-001", "name": "Workstation Pro", "price": 1299.99, "category_name": "Computers"},
    {"sku": "MOU-002", "name": "Wireless Mouse", "price": 49.99, "category_name": "Accessories"},
    {"sku": "KEY-003", "name": "Mechanical Keyboard", "price": 129.99, "category_name": "Accessories"},
    {"sku": "MON-004", "name": "4K Ultra-Wide Monitor", "price": 499.99, "category_name": "Display"},
    {"sku": "HEAD-005", "name": "Noise Cancelling Headphones", "price": 299.99, "category_name": "Audio"},
]

CUSTOMERS = [
    "alice@example.com", "bob@test.org", "charlie@demo.net", 
    "dana@web.com", "evie@store.io", "frank@retail.com"
]

async def wait_for_api(client: httpx.AsyncClient):
    logger.info(f"Waiting for API at {API_URL}...")
    while True:
        try:
            response = await client.get(f"{API_URL}/health")
            if response.status_code == 200:
                logger.info("API is up!")
                return
        except Exception:
            pass
        await asyncio.sleep(2)

async def seed_products(client: httpx.AsyncClient):
    logger.info("Checking for products...")
    response = await client.get(f"{API_URL}/api/products/")
    products = response.json()
    
    if not products:
        logger.info("No products found. Seeding demo catalog...")
        for p in DEMO_PRODUCTS:
            try:
                await client.post(f"{API_URL}/api/products/", json=p)
                logger.info(f"Seeded: {p['name']}")
            except Exception as e:
                logger.error(f"Failed to seed {p['name']}: {e}")
        
        # Refresh product list
        response = await client.get(f"{API_URL}/api/products/")
        products = response.json()
    
    return products

async def run_simulation():
    async with httpx.AsyncClient(timeout=10.0) as client:
        await wait_for_api(client)
        products = await seed_products(client)
        
        if not products:
            logger.error("No products available to simulate. Exiting.")
            sys.exit(1)

        logger.info(f"Simulation started with profile: {SIM_PROFILE}")
        
        while True:
            try:
                # Randomize order
                num_items = random.randint(1, 3)
                selected_products = random.sample(products, num_items)
                
                order_items = []
                for p in selected_products:
                    order_items.append({
                        "product_id": p["id"],
                        "quantity": random.randint(1, 5),
                        "unit_price": p["price"]
                    })
                
                payload = {
                    "customer_email": random.choice(CUSTOMERS),
                    "items": order_items
                }
                
                response = await client.post(f"{API_URL}/api/orders/", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"Order Created: {data['order_id']} | Msg: {data['msg_id']}")
                else:
                    logger.error(f"Failed to create order: {response.status_code} - {response.text}")

            except Exception as e:
                logger.error(f"Error in simulation loop: {e}")

            # Sleep based on profile
            if SIM_PROFILE == "BURST":
                await asyncio.sleep(random.uniform(0.1, 0.5))
            else:
                await asyncio.sleep(random.uniform(2.0, 5.0))

if __name__ == "__main__":
    try:
        asyncio.run(run_simulation())
    except KeyboardInterrupt:
        logger.info("Simulator stopped.")
