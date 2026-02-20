from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.services.analytics import analytics_service
import asyncio
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/dashboard")
async def websocket_endpoint(websocket: WebSocket):
    print(f"WebSocket connection attempt from {websocket.client}")
    await manager.connect(websocket)
    print("WebSocket accepted")
    try:
        while True:
            # Push updates every 2 seconds
            stats = await analytics_service.get_dashboard_stats()
            await websocket.send_text(json.dumps(stats))
            await asyncio.sleep(2)
            
            # Keep alive check / read message (though we don't expect client messages)
            # try:
            #     data = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
            # except asyncio.TimeoutError:
            #     pass
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
