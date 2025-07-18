from typing import Annotated

from clickhouse_connect.driver import AsyncClient as AsyncClickHouseClient
from fastapi.params import Depends

from pypi_clickhouse_analytics.clients import CacheClient
from pypi_clickhouse_analytics.dependencies.clients import (
    get_cache_client,
    get_clickhouse_client,
)
from pypi_clickhouse_analytics.repos import PypiCacheRepo, PyPiProjectAnalyticsRepo


async def get_pypi_analytics_repo(
    clickhouse_client: Annotated[AsyncClickHouseClient, Depends(get_clickhouse_client)],
) -> PyPiProjectAnalyticsRepo:
    return PyPiProjectAnalyticsRepo(clickhouse_client)


def get_pypi_cache_repo(
    cache: Annotated[CacheClient, Depends(get_cache_client)],
) -> PypiCacheRepo:
    return PypiCacheRepo(cache)
