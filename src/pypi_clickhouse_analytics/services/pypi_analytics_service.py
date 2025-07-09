from datetime import datetime

from pypi_clickhouse_analytics.entities.projects import ProjectDownloads, GroupedDownloads, GroupedDownloadItem
from pypi_clickhouse_analytics.enums.group_by_enum import GroupByColumn
from pypi_clickhouse_analytics.repos import PyPiProjectAnalyticsRepo


class PyPiAnalyticsService:
    def __init__(self, pypi_analytics_repo: PyPiProjectAnalyticsRepo):
        self.__pypi_analytics_repo = pypi_analytics_repo

    async def get_project_download_count(
        self,
        project_name: str,
        *,
        from_dt: datetime | None = None,
        to_dt: datetime | None = None
    ) -> ProjectDownloads:
        download_count: int = await self.__pypi_analytics_repo.get_download_count(
            project_name, from_dt=from_dt, to_dt=to_dt
        )
        return ProjectDownloads(downloads=download_count)

    async def group_project_downloads(
        self,
        project_name: str,
        group_by_column: GroupByColumn,
        *,
        from_dt: datetime | None = None,
        to_dt: datetime | None = None
    ) -> GroupedDownloads:
        downloads = await self.__pypi_analytics_repo.group_downloads(
            project_name, group_by_column=group_by_column, from_dt=from_dt, to_dt=to_dt
        )
        return GroupedDownloads(
            grouped_by=group_by_column,
            items=(
                GroupedDownloadItem(value=item[group_by_column], downloads=item["DOWNLOAD_COUNT"])
                for item in downloads
            )
        )
