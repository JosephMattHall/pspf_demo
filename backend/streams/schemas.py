from pspf import BaseEvent
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import Field, field_validator

class StreamStockEvent(BaseEvent):
    """Base class for all StreamStock events to ensure common metadata."""
    source: str = "streamstock.backend"
    version: str = "1.0"

    @field_validator("version", mode="before")
    @classmethod
    def coerce_version(cls, v):
        if v is None:
            return "1.0"
        return str(v)

# We'll add specific events here as we define them in Phase 2
