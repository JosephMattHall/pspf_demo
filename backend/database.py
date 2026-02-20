from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from backend.config.settings import settings

# Create Async Engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True
)

# Create Session Factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Base is now imported from models.base when needed for migrations

# Dependency for FastAPI
async def get_db():

    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
