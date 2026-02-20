from pydantic import Field, UUID4, BaseModel
from typing import List
from backend.streams.schemas import StreamStockEvent

# Inventory Events

class ProductCreated(StreamStockEvent):
    event_type: str = "product.created"
    product_id: UUID4
    sku: str
    name: str
    price: float
    category_id: UUID4 | None = None

class StockReceived(StreamStockEvent):
    event_type: str = "stock.received"
    product_id: UUID4
    quantity: int
    location: str = "WAREHOUSE_1"

class StockReserved(StreamStockEvent):
    event_type: str = "stock.reserved"
    order_id: UUID4
    product_id: UUID4
    quantity: int

class LowStockAlert(StreamStockEvent):
    event_type: str = "stock.low"
    product_id: UUID4
    current_quantity: int
    threshold: int

# Order Events

class OrderItemSchema(BaseModel):
    product_id: UUID4
    quantity: int
    unit_price: float

class OrderCreated(StreamStockEvent):
    event_type: str = "order.created"
    order_id: UUID4
    customer_email: str
    items: List[OrderItemSchema]
    total_amount: float

class OrderConfirmed(StreamStockEvent):
    event_type: str = "order.confirmed"
    order_id: UUID4
    timestamp: str

class OrderCancelled(StreamStockEvent):
    event_type: str = "order.cancelled"
    order_id: UUID4
    reason: str
