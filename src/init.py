from src.connectors.redis_connectors import RedisConnector
from src.database import settings


redis_manager = RedisConnector(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT
)
