import asyncio
import logging
from backend.config.settings import settings
from backend.streams.client import stream_client
from backend.processors.inventory import process_inventory_event
from backend.processors.orders import process_order_event
from backend.processors.restock import process_restock_event
from backend.processors.analytics import process_analytics_event
from backend.processors.alerts import process_alert_event
from backend.processors.audit import process_audit_event
from pspf import BatchProcessor

# Setup logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger("Worker")

async def main():
    logger.info("Starting StreamStock Wrappers...")
    
    # Connect Backend
    await stream_client.connect()
    
    # Initialize Processor
    # In this simple model, we use one processor instance to poll the stream.
    # It dispatches to specific handlers based on event_type.
    # Alternatively, we could have multiple processors (consumer groups) for different domains.
    # For simplicity, we use one "Monolith Worker" group here, but dispatch logic inside.
    
    processor = BatchProcessor(stream_client.backend)
    
    async def global_dispatcher(msg_id, data, ctx=None):
        # Dispatch to all handlers
        # In a real app, you might want separate consumer groups for Inventory vs Orders 
        # so they can scale independently. 
        # Here we run them sequentially for the same message (fan-out logic inside app)
        # OR we check event type.
        
        # NOTE: If we use the SAME consumer group, the message is delivered ONCE to one worker.
        # So this worker needs to run ALL logic for that event.
        
        await process_inventory_event(msg_id, data, ctx)
        await process_order_event(msg_id, data, ctx)
        await process_restock_event(msg_id, data, ctx)
        await process_analytics_event(msg_id, data, ctx)
        await process_alert_event(msg_id, data, ctx)
        await process_audit_event(msg_id, data, ctx)

    try:
        await processor.run_loop(global_dispatcher)
    except KeyboardInterrupt:
        await processor.shutdown()
    finally:
        await stream_client.close()

if __name__ == "__main__":
    asyncio.run(main())
