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

# Setup logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger("Worker")

async def main():
    logger.info("Starting StreamStock Wrappers...")
    
    # Connect Backend
    await stream_client.connect()
    
# Initialize Subscriptions
# In 0.1.0b1, we can use the @subscribe decorator on the stream object.
@stream_client.stream.subscribe("streamstock.events")
async def global_dispatcher(msg_id, data, ctx=None):
    # Dispatch to all handlers
    await process_inventory_event(msg_id, data, ctx)
    await process_order_event(msg_id, data, ctx)
    await process_restock_event(msg_id, data, ctx)
    await process_analytics_event(msg_id, data, ctx)
    await process_alert_event(msg_id, data, ctx)
    await process_audit_event(msg_id, data, ctx)

async def main():
    logger.info("Starting StreamStock Workers (0.1.0b1 pattern)...")
    
    # Connect Backend
    await stream_client.connect()
    
    try:
        # run_forever handles all registered subscriptions concurrently
        await stream_client.stream.run_forever()
    except asyncio.CancelledError:
        logger.info("Worker loop stopped.")
    finally:
        await stream_client.close()

if __name__ == "__main__":
    asyncio.run(main())
