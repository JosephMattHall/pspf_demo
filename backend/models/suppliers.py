from uuid import UUID as PyUUID, uuid4
from enum import Enum
from sqlalchemy import String, Integer, ForeignKey, Float, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import TimestampedModel

class PurchaseOrderStatus(str, Enum):
    DRAFT = "DRAFT"
    ORDERED = "ORDERED"
    RECEIVED = "RECEIVED"
    CANCELLED = "CANCELLED"

class Supplier(TimestampedModel):
    __tablename__ = "suppliers"
    
    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    contact_email: Mapped[str | None] = mapped_column(String, nullable=True)
    
    purchase_orders: Mapped[list["PurchaseOrder"]] = relationship(back_populates="supplier")

class PurchaseOrder(TimestampedModel):
    __tablename__ = "purchase_orders"
    
    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    supplier_id: Mapped[PyUUID] = mapped_column(ForeignKey("suppliers.id"))
    status: Mapped[PurchaseOrderStatus] = mapped_column(SAEnum(PurchaseOrderStatus), default=PurchaseOrderStatus.DRAFT)
    total_amount: Mapped[float] = mapped_column(Float, default=0.0)
    
    supplier: Mapped["Supplier"] = relationship(back_populates="purchase_orders")
    # simplified: items logic would be similar to OrderItem, keeping it simple for now
