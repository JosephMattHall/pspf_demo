from pspf import BatchProcessor
from pspf.context import Context
from backend.streams.events import OrderCreated, StockReceived, StockReserved, LowStockAlert, ProductCreated
from backend.services.inventory import InventoryService
from backend.database import AsyncSessionLocal
from backend.streams.client import stream_client
from backend.streams.events import OrderCancelled
import logging

logger = logging.getLogger("InventoryProcessor")

async def process_inventory_event(msg_id, data, ctx: Context):
    event_type = data.get("event_type")
    logger.info(f"Processing event: {event_type} | ID: {msg_id}")

    async with AsyncSessionLocal() as session:
        service = InventoryService(session)
        
        if event_type == "stock.received":
            # 1. Handle Stock Receipt
            # We validate schema manually here or trust the upstream
            # ideally use pydantic to parse
            try:
                event = StockReceived(**data)
                await service.add_stock(event.product_id, event.quantity)
                logger.info(f"Added {event.quantity} stock for {event.product_id}")
            except Exception as e:
                logger.error(f"Failed to process stock.received: {e}")

        elif event_type == "order.created":
            # 2. Reserve Stock for Order
            # Implementing Optimistic Reservation
            try:
                event = OrderCreated(**data)
                all_reserved = True
                
                # Try to reserve all items
                # Transactional note: In a real system, we might want to lock rows. 
                # Here we do sequential checks.
                
                for item in event.items:
                    success = await service.reserve_stock(item.product_id, item.quantity)
                    if success:
                        # Emit Reserved Event
                        reserved_event = StockReserved(
                            order_id=event.order_id,
                            product_id=item.product_id,
                            quantity=item.quantity
                        )
                        await stream_client.stream.emit(reserved_event)
                        logger.info(f"Reserved {item.quantity} of {item.product_id} for Order {event.order_id}")
                    else:
                        all_reserved = False
                        logger.warning(f"Insufficient stock for {item.product_id} (Order {event.order_id})")
                        # Here we should probably trigger a compensation (Order Failed)
                        # We emit an OrderCancelled or OrderFailed event
                        fail_event = OrderCancelled(
                            order_id=event.order_id,
                            reason=f"Insufficient stock for product {item.product_id}"
                        )
                        await stream_client.stream.emit(fail_event)
                        break # Stop processing this order
                
                # If we failed mid-way, we strictly should rollback previous reservations for this order.
                # For this simplified demo, we'll implement that compensation logic in a robust version later.
                
            except Exception as e:
                logger.error(f"Failed to process order.created: {e}")

        elif event_type == "product.created":
             # Initialize inventory record with some starting stock for the demo
             try:
                 event = ProductCreated(**data)
                 await service.add_stock(event.product_id, 100) # Give 100 initial stock
                 logger.info(f"Initialized inventory for {event.product_id} with 100 units")
             except Exception as e:
                 logger.error(f"Failed to process product.created: {e}")

