from pspf import BatchProcessor
from pspf.context import Context
import logging
import json

# Configure specific logger for audit
audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)
# Basic config for demo purposes, in prod this might go to S3/Splunk
handler = logging.FileHandler("audit.log")
handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
audit_logger.addHandler(handler)

async def process_audit_event(msg_id, data, ctx: Context):
    # This processor listens to everything or specific audit topics
    # For the demo, we hook it into the main dispatcher
    
    event_type = data.get("event_type", "unknown")
    event_id = data.get("event_id", "unknown")
    
    # Structured log entry
    entry = {
        "timestamp": data.get("timestamp"),
        "event_id": event_id,
        "type": event_type,
        "payload": data
    }
    
    audit_logger.info(json.dumps(entry))
