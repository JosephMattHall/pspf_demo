from pspf import BatchProcessor
from pspf.context import Context
from backend.streams.events import OrderCreated, StockReceived, StockReserved
from backend.services.analytics import analytics_service
import logging

logger = logging.getLogger("AnalyticsProcessor")

async def process_analytics_event(msg_id, data, ctx: Context):
    event_type = data.get("event_type")
    
    try:
        if event_type == "order.created":
            event = OrderCreated(**data)
            await analytics_service.increment_sales(event.total_amount)
            logger.info(f"Updated sales analytics for Order {event.order_id}")
            
        elif event_type == "stock.received":
            event = StockReceived(**data)
            await analytics_service.update_stock_level(str(event.product_id), event.quantity)
            
        elif event_type == "stock.reserved":
            # For accurate stock levels, we should decrement
            # But we might need current level from event payload.
            # Simplified: just log for now or assume we get snapshot events.
            pass
            
    except Exception as e:
        logger.error(f"Analytics processing failed: {e}")
