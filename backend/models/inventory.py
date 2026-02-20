from uuid import UUID as PyUUID, uuid4
from sqlalchemy import String, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import TimestampedModel

class Category(TimestampedModel):
    __tablename__ = "categories"
    
    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

    products: Mapped[list["Product"]] = relationship(back_populates="category")

class Product(TimestampedModel):
    __tablename__ = "products"
    
    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    sku: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    price: Mapped[float] = mapped_column(Float)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    
    category_id: Mapped[PyUUID | None] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="products")
    
    inventory_items: Mapped[list["InventoryItem"]] = relationship(back_populates="product")

class InventoryItem(TimestampedModel):
    __tablename__ = "inventory_items"
    
    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    product_id: Mapped[PyUUID] = mapped_column(ForeignKey("products.id"), index=True)
    location: Mapped[str] = mapped_column(String, default="WAREHOUSE_1")
    
    quantity_on_hand: Mapped[int] = mapped_column(Integer, default=0)
    quantity_reserved: Mapped[int] = mapped_column(Integer, default=0)
    
    product: Mapped["Product"] = relationship(back_populates="inventory_items")
