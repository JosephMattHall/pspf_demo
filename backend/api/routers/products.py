from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import uuid4
from backend.database import get_db
from backend.models.inventory import Product, Category
from backend.streams.dependencies import get_stream
from backend.streams.events import ProductCreated
from pspf import Stream
from pydantic import BaseModel

router = APIRouter()

class ProductCreate(BaseModel):
    sku: str
    name: str
    price: float
    description: str | None = None
    category_name: str | None = None

from uuid import uuid4, UUID

class ProductResponse(BaseModel):
    id: UUID
    sku: str
    name: str
    price: float
    
    class Config:
        from_attributes = True

@router.post("/", response_model=ProductResponse)
async def create_product(
    product_in: ProductCreate, 
    db: AsyncSession = Depends(get_db),
    stream: Stream = Depends(get_stream)
):
    # 1. Create DB Record (Read Model)
    # We create it in DB immediately for read-after-write consistency in this simple demo
    # Ideally, we'd wait for the event processor to create it, but that makes UI harder.
    # Hybrid approach: Write to DB PENDING, Emit Event, Processor updates to ACTIVE.
    
    # For this demo: Write to DB, Emit Event (which initializes inventory).
    
    new_product_id = uuid4()
    product = Product(
        id=new_product_id,
        sku=product_in.sku,
        name=product_in.name,
        price=product_in.price,
        description=product_in.description
    )
    db.add(product)
    await db.commit()
    await db.refresh(product)
    
    # 2. Emit Event
    event = ProductCreated(
        product_id=new_product_id,
        sku=product.sku,
        name=product.name,
        price=product.price
    )
    await stream.emit(event)
    
    return product

@router.get("/", response_model=list[ProductResponse])
async def list_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return products
