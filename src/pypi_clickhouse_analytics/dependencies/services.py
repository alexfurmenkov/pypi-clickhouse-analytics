from typing import Annotated

from fastapi.params import Depends

from pypi_clickhouse_analytics.dependencies.repos import get_pypi_analytics_repo
from pypi_clickhouse_analytics.repos import PyPiProjectAnalyticsRepo
from pypi_clickhouse_analytics.services.pypi_analytics_service import PyPiAnalyticsService


async def get_pypi_analytics_service(
    pypi_analytics_repo: Annotated[PyPiProjectAnalyticsRepo, Depends(get_pypi_analytics_repo)]
) -> PyPiAnalyticsService:
    return PyPiAnalyticsService(pypi_analytics_repo)
