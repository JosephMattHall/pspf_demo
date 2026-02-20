import asyncio
import logging
from backend.database import engine
from backend.models.base import Base
# Import all models to register them with Base.metadata
from backend.models.inventory import Product, Category
from backend.models.orders import Order, OrderItem
from backend.models.suppliers import Supplier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("InitDB")

async def init_db():
    logger.info("Initializing database...")
    async with engine.begin() as conn:
        # Create all tables
        # For a production app, use migrations (Alembic)
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized successfully!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())
