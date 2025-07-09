from datetime import datetime

from pypi_clickhouse_analytics.entities.projects import ProjectDownloads
from pypi_clickhouse_analytics.repos import PyPiAnalyticsRepo


class PyPiAnalyticsService:
    def __init__(self, pypi_analytics_repo: PyPiAnalyticsRepo):
        self.__pypi_analytics_repo = pypi_analytics_repo

    async def get_project_download_count(
        self,
        project_name: str,
        from_dt: datetime | None = None,
        to_dt: datetime | None = None
    ) -> ProjectDownloads:
        download_count: int = await self.__pypi_analytics_repo.get_project_download_count(project_name, from_dt, to_dt)
        return ProjectDownloads(downloads=download_count)
