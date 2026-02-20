from pspf import BatchProcessor
from pspf.context import Context
from backend.streams.events import LowStockAlert
from backend.services.inventory import InventoryService
from backend.database import AsyncSessionLocal
import logging

logger = logging.getLogger("RestockProcessor")

async def process_restock_event(msg_id, data, ctx: Context):
    event_type = data.get("event_type")
    
    if event_type == "stock.low":
        try:
            event = LowStockAlert(**data)
            logger.info(f"Low stock alert for {event.product_id}. Current: {event.current_quantity}")
            
            # Logic to create a Purchase Order would go here
            # For now, just log it as a TODO
            # 1. Check if open PO exists for this product
            # 2. If not, create new PO
            
            logger.info(f"Generated Purchase Order Draft for Product {event.product_id}")
            
        except Exception as e:
            logger.error(f"Failed to process stock.low: {e}")
