from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from backend.database import get_db
from backend.streams.dependencies import get_stream
from backend.streams.events import OrderCreated, OrderItemSchema
from pspf import Stream
from pydantic import BaseModel

router = APIRouter()

class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int
    unit_price: float

class OrderCreateRequest(BaseModel):
    customer_email: str
    items: list[OrderItemCreate]

@router.post("/")
async def create_order(
    order_in: OrderCreateRequest,
    stream: Stream = Depends(get_stream)
):
    # We DO NOT write to DB here. 
    # We adhere to "Events First" for Orders to demonstrate the pattern.
    # The OrderProcessor will consume the event and create the DB record.
    
    order_id = uuid4()
    
    event = OrderCreated(
        order_id=order_id,
        customer_email=order_in.customer_email,
        items=[
            OrderItemSchema(
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price
            ) for item in order_in.items
        ],
        total_amount=sum(i.quantity * i.unit_price for i in order_in.items)
    )
    
    msg_id = await stream.emit(event)
    
    return {"order_id": str(order_id), "status": "QUEUED", "msg_id": msg_id}
