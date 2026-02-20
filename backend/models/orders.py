from uuid import UUID as PyUUID, uuid4
from enum import Enum
from sqlalchemy import String, Integer, Float, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import TimestampedModel

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class Order(TimestampedModel):
    __tablename__ = "orders"
    
    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_email: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[OrderStatus] = mapped_column(SAEnum(OrderStatus), default=OrderStatus.PENDING)
    total_amount: Mapped[float] = mapped_column(Float, default=0.0)
    
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")

class OrderItem(TimestampedModel):
    __tablename__ = "order_items"
    
    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    order_id: Mapped[PyUUID] = mapped_column(ForeignKey("orders.id"), index=True)
    product_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), index=True) # Direct ID reference, could link to Product
    
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(Float)
    
    order: Mapped["Order"] = relationship(back_populates="items")
