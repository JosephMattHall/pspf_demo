from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from backend.models.inventory import InventoryItem, Product
from uuid import UUID

class InventoryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_item(self, product_id: UUID) -> InventoryItem | None:
        result = await self.session.execute(
            select(InventoryItem).where(InventoryItem.product_id == product_id)
        )
        return result.scalars().first()

    async def add_stock(self, product_id: UUID, quantity: int, location: str = "WAREHOUSE_1"):
        item = await self.get_item(product_id)
        if not item:
            item = InventoryItem(product_id=product_id, location=location, quantity_on_hand=0)
            self.session.add(item)
        
        item.quantity_on_hand += quantity
        await self.session.commit()
        return item

    async def reserve_stock(self, product_id: UUID, quantity: int) -> bool:
        """
        Attempts to reserve stock. Returns True if successful, False if insufficient stock.
        """
        item = await self.get_item(product_id)
        if not item:
            return False
        
        available = item.quantity_on_hand - item.quantity_reserved
        if available >= quantity:
            item.quantity_reserved += quantity
            await self.session.commit()
            return True
        return False

    async def confirm_reservation(self, product_id: UUID, quantity: int):
        """
        Deducts from both on_hand and reserved. Called when order is finalized/shipped.
        """
        item = await self.get_item(product_id)
        if item:
            item.quantity_on_hand -= quantity
            item.quantity_reserved -= quantity
            await self.session.commit()

    async def cancel_reservation(self, product_id: UUID, quantity: int):
        """
        Returns stock to available pool (decrements reserved).
        """
        item = await self.get_item(product_id)
        if item:
            item.quantity_reserved -= quantity
            await self.session.commit()
