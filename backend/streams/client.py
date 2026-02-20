from urllib.parse import urlparse
from pspf.connectors.valkey import ValkeyStreamBackend, ValkeyConnector
from pspf import Stream
from backend.config.settings import settings
import socket
import os

class StreamClient:
    def __init__(self):
        # Parse Redis URL
        parsed = urlparse(settings.redis_url)
        host = parsed.hostname or 'localhost'
        port = parsed.port or 6379
        db = int(parsed.path.lstrip('/')) if parsed.path else 0
        password = parsed.password

        # Create Connector
        self.connector = ValkeyConnector(host=host, port=port, password=password, db=db)
        
        # Determine consumer name
        consumer_name = f"{socket.gethostname()}-{os.getpid()}"

        self.backend = ValkeyStreamBackend(
            connector=self.connector,
            stream_key="streamstock.events",
            group_name="streamstock.workers",
            consumer_name=consumer_name
        )
        self.stream = Stream(backend=self.backend)

    async def connect(self):
        await self.backend.connect()
        await self.backend.ensure_group_exists()

    async def close(self):
        await self.backend.close()

# Global instance
stream_client = StreamClient()
