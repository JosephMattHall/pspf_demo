from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from backend.models.orders import Order, OrderItem, OrderStatus
from uuid import UUID

class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, order_id: UUID, customer_email: str, items_data: list) -> Order:
        order = Order(
            id=order_id,
            customer_email=customer_email,
            status=OrderStatus.PENDING,
            total_amount=0.0 # Calculate later
        )
        self.session.add(order)
        
        total = 0.0
        for item_data in items_data:
            item = OrderItem(
                order_id=order_id,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price']
            )
            total += item.quantity * item.unit_price
            self.session.add(item)
        
        order.total_amount = total
        await self.session.commit()
        return order

    async def update_status(self, order_id: UUID, status: OrderStatus):
        stmt = update(Order).where(Order.id == order_id).values(status=status)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_order(self, order_id: UUID) -> Order | None:
        result = await self.session.execute(select(Order).where(Order.id == order_id))
        return result.scalars().first()
