import redis.asyncio as redis


class RedisConnector:
    """"Управление Redis."""
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        self.redis = await redis.Redis(host=self.host, port=self.port)

    async def set(self, key: str, value: str, expire: int | None = None):
        if expire and self.redis:
            await self.redis.set(key, value, ex=expire)
        elif expire is None and self.redis:
            await self.redis.set(key, value)

    async def get(self, key: str):
        if self.redis:
            return await self.redis.get(key)

    async def delete(self, key: str):
        if self.redis:
            await self.redis.delete(key)

    async def close(self):
        if self.redis:
            await self.redis.close()
