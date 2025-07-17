from typing import Annotated

import clickhouse_connect
from fastapi.params import Depends

from pypi_clickhouse_analytics.app_settings import settings
from pypi_clickhouse_analytics.clients import CacheClient
from pypi_clickhouse_analytics.dependencies.clients import get_cache_client
from pypi_clickhouse_analytics.repos import PypiCacheRepo, PyPiProjectAnalyticsRepo


async def get_pypi_analytics_repo() -> PyPiProjectAnalyticsRepo:
    client = await clickhouse_connect.get_async_client(
        host=settings.CLICKHOUSE_HOST,
        username=settings.CLICKHOUSE_USER,
        password=settings.CLICKHOUSE_PASS,
        database=settings.CLICKHOUSE_DB,
        port=settings.CLICKHOUSE_PORT,
    )
    return PyPiProjectAnalyticsRepo(client)


def get_pypi_cache_repo(
    cache: Annotated[CacheClient, Depends(get_cache_client)],
) -> PypiCacheRepo:
    return PypiCacheRepo(cache)
