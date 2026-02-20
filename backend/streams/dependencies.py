from backend.streams.client import stream_client

async def get_stream():
    # In a real app, you might want to manage connection lifecycle 
    # via lifespan events in main.py, but this dependency checks connection.
    # Ideally, connection is established at startup.
    return stream_client.stream
