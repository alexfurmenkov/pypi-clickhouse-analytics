from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi.params import Depends
from httpx import AsyncClient, Timeout
from redis.asyncio import Redis
from redis.exceptions import ConnectionError

from pypi_clickhouse_analytics.app_settings import settings
from pypi_clickhouse_analytics.clients import (
    CacheClient,
    LocalCache,
    PyPiAPIClient,
    RedisCache,
)


async def get_httpx_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        timeout=Timeout(settings.HTTPX_TIMEOUT),
    ) as client:
        yield client


async def get_pypi_api_client(
    http_client: Annotated[AsyncClient, Depends(get_httpx_client)],
) -> PyPiAPIClient:
    return PyPiAPIClient(http_client)


async def get_cache_client() -> CacheClient:
    redis_client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        username=settings.REDIS_USERNAME,
        password=settings.REDIS_PASSWORD,
    )
    try:
        await redis_client.ping()
    except ConnectionError:
        return LocalCache()

    return RedisCache(redis_client)
