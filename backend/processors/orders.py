from pspf import BatchProcessor
from pspf.context import Context
from backend.streams.events import OrderCreated, OrderConfirmed, OrderCancelled
from backend.services.orders import OrderService, OrderStatus
from backend.database import AsyncSessionLocal
import logging

logger = logging.getLogger("OrderProcessor")

async def process_order_event(msg_id, data, ctx: Context):
    event_type = data.get("event_type")
    
    async with AsyncSessionLocal() as session:
        service = OrderService(session)

        if event_type == "order.created":
            try:
                # Idempotency check: verify if order already exists
                # (Assuming order_id is provied by upstream/API)
                event = OrderCreated(**data)
                existing = await service.get_order(event.order_id)
                if not existing:
                    # Create PENDING order
                    items_dicts = [item.dict() for item in event.items]
                    await service.create_order(
                        order_id=event.order_id,
                        customer_email=event.customer_email,
                        items_data=items_dicts
                    )
                    logger.info(f"Created Order {event.order_id} (PENDING)")
                else:
                    logger.info(f"Order {event.order_id} alread exists. Skipping creation.")
            except Exception as e:
                logger.error(f"Failed to process order.created: {e}")

        elif event_type == "order.confirmed":
            try:
                event = OrderConfirmed(**data)
                # Update status to CONFIRMED
                await service.update_status(event.order_id, OrderStatus.CONFIRMED)
                logger.info(f"Order {event.order_id} confirmed.")
            except Exception as e:
                logger.error(f"Failed to process order.confirmed: {e}")

        elif event_type == "order.cancelled":
            try:
                event = OrderCancelled(**data)
                # Update status to CANCELLED
                await service.update_status(event.order_id, OrderStatus.CANCELLED)
                logger.info(f"Order {event.order_id} cancelled: {event.reason}")
                
                # TODO: Trigger compensation to release reserved stock
            except Exception as e:
                logger.error(f"Failed to process order.cancelled: {e}")
