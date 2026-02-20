from redis.asyncio import Redis
from backend.config.settings import settings

class AnalyticsService:
    def __init__(self):
        self.redis = Redis.from_url(settings.redis_url, decode_responses=True)

    async def increment_sales(self, amount: float):
        # Daily Sales
        await self.redis.incrbyfloat("analytics:sales:today", amount)
        # Total Sales
        await self.redis.incrbyfloat("analytics:sales:total", amount)
        # Order Count
        await self.redis.incr("analytics:orders:count")

    async def update_stock_level(self, product_id: str, quantity: int):
        # We might store a hash of stock levels for heatmap
        await self.redis.hset("analytics:stock:levels", product_id, quantity)

    async def get_dashboard_stats(self):
        total_sales = await self.redis.get("analytics:sales:total") or 0.0
        today_sales = await self.redis.get("analytics:sales:today") or 0.0
        order_count = await self.redis.get("analytics:orders:count") or 0
        
        return {
            "total_sales": float(total_sales),
            "today_sales": float(today_sales),
            "order_count": int(order_count)
        }

analytics_service = AnalyticsService()
