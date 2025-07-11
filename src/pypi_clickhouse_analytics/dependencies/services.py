from typing import Annotated

from fastapi.params import Depends

from pypi_clickhouse_analytics.clients.pypi_api_client import PyPiAPIClient
from pypi_clickhouse_analytics.dependencies.clients import get_pypi_api_client
from pypi_clickhouse_analytics.dependencies.repos import get_pypi_analytics_repo, get_pypi_cache_repo
from pypi_clickhouse_analytics.repos import PyPiProjectAnalyticsRepo
from pypi_clickhouse_analytics.repos.pypi_cache_repo import PypiCacheRepo
from pypi_clickhouse_analytics.services.pypi_analytics_service import PyPiAnalyticsService


def get_pypi_analytics_service(
    pypi_analytics_repo: Annotated[PyPiProjectAnalyticsRepo, Depends(get_pypi_analytics_repo)],
    pypi_api_client: Annotated[PyPiAPIClient, Depends(get_pypi_api_client)],
    pypi_cache_repo: Annotated[PypiCacheRepo, Depends(get_pypi_cache_repo)]
) -> PyPiAnalyticsService:
    return PyPiAnalyticsService(pypi_analytics_repo, pypi_api_client, pypi_cache_repo)
