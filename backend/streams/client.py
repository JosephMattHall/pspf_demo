from pspf import Stream
from backend.config.settings import settings

class StreamClient:
    def __init__(self):
        # In 0.1.0b1, providing topic and group enables auto-instantiation
        # of the backend based on global settings (env vars).
        self.stream = Stream(
            topic="streamstock.events",
            group="streamstock.workers"
        )
        self.backend = self.stream.backend

    async def connect(self):
        await self.backend.connect()
        # ensure_group_exists is handled by the backend internally in 0.1.0b1 
        # but we can keep the explicit call if the backend supports it.
        if hasattr(self.backend, "ensure_group_exists"):
            await self.backend.ensure_group_exists()

    async def close(self):
        await self.backend.close()

# Global instance
stream_client = StreamClient()
