import redis

from app.core.config import settings


redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    decode_responses=True,
)


def cache_device_status(device_id: int, online_status: str, sync_status: str, offset: float) -> None:
    redis_client.hset(
        f"device:{device_id}",
        mapping={
            "online_status": online_status,
            "sync_status": sync_status,
            "offset": offset,
        },
    )
