from pspf import BatchProcessor
from pspf.context import Context
from backend.streams.events import LowStockAlert, StreamStockEvent
from redis.asyncio import Redis
from backend.config.settings import settings
import logging
import json
import time

logger = logging.getLogger("AlertProcessor")
redis = Redis.from_url(settings.redis_url, decode_responses=True)

class AlertTriggered(StreamStockEvent):
    event_type: str = "alert.triggered"
    severity: str # INFO, WARNING, CRITICAL
    message: str
    related_id: str | None = None

async def process_alert_event(msg_id, data, ctx: Context):
    event_type = data.get("event_type")
    
    alert = None
    
    if event_type == "stock.low":
        try:
            event = LowStockAlert(**data)
            alert = AlertTriggered(
                severity="WARNING",
                message=f"Low stock for Product {event.product_id}. On Hand: {event.current_quantity}",
                related_id=str(event.product_id)
            )
        except Exception as e:
             logger.error(f"Failed to process alert source: {e}")

    elif event_type == "order.cancelled":
        # We can treat cancellation as an alert too
        reason = data.get("reason", "Unknown")
        oid = data.get("order_id", "Unknown")
        alert = AlertTriggered(
            severity="info",
            message=f"Order {oid} cancelled: {reason}",
            related_id=oid
        )

    if alert:
        # 1. Log
        logger.warning(f"ALERT: {alert.message}")
        
        # 2. Store in Redis List for Dashboard Feed (capped at 50)
        alert_json = alert.model_dump_json()
        await redis.lpush("alerts:feed", alert_json)
        await redis.ltrim("alerts:feed", 0, 49)
        
        # 3. Publish to PubSub for immediate WebSocket push (optional, if we wire WS to PubSub)
        # For now, WS polls or we can push to a specific channel the WS listens to.
        # Let's push to redis pubsub so the WS router can subscribe if improved later.
        await redis.publish("alerts", alert_json)
