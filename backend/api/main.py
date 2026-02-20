from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config.settings import settings
from backend.api.routers import products, orders, websocket
from backend.streams.client import stream_client

app = FastAPI(title=settings.project_name)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In prod, be specific
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup/Shutdown Events
@app.on_event("startup")
async def startup_event():
    await stream_client.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await stream_client.close()

# Routers
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])

@app.get("/health")
async def health():
    return {"status": "ok"}
