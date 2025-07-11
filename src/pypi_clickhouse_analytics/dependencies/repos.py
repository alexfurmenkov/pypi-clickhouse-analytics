import clickhouse_connect

from pypi_clickhouse_analytics.app_settings import settings
from pypi_clickhouse_analytics.repos import PyPiProjectAnalyticsRepo


async def get_pypi_analytics_repo() -> PyPiProjectAnalyticsRepo:
    client = await clickhouse_connect.get_async_client(
        host=settings.CLICKHOUSE_HOST,
        username=settings.CLICKHOUSE_USER,
        password=settings.CLICKHOUSE_PASS,
        database=settings.CLICKHOUSE_DB,
        port=settings.CLICKHOUSE_PORT,
    )
    return PyPiProjectAnalyticsRepo(client)
