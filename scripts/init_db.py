import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from backend.config.settings import settings
from backend.models.base import Base
# Import all models to ensure they are registered with Base metadata
from backend.models import * 

async def init_db():
    print(f"Connecting to {settings.database_url}...")
    engine = create_async_engine(settings.database_url, echo=True)
    
    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully!")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())
