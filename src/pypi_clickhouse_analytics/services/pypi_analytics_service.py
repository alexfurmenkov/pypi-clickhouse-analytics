from datetime import datetime
from typing import Any

from pypi_clickhouse_analytics.clients.pypi_api_client import PyPiAPIClient
from pypi_clickhouse_analytics.entities.projects import ProjectDownloads, GroupedDownloads, GroupedDownloadItem, \
    ProjectMeta
from pypi_clickhouse_analytics.enums.group_by_enum import GroupByColumn
from pypi_clickhouse_analytics.repos import PyPiProjectAnalyticsRepo
from pypi_clickhouse_analytics.repos.pypi_cache_repo import PypiCacheRepo


class PyPiAnalyticsService:
    def __init__(
        self,
        pypi_analytics_repo: PyPiProjectAnalyticsRepo,
        pypi_api_client: PyPiAPIClient,
        pypi_cache_repo: PypiCacheRepo,
    ):
        self.__pypi_analytics_repo = pypi_analytics_repo
        self.__pypi_api_client = pypi_api_client
        self.__pypi_cache_repo = pypi_cache_repo

    async def get_project_meta(self, project_name: str) -> ProjectMeta:
        cached: ProjectMeta | None = await self.__pypi_cache_repo.get_project_meta(project_name)
        if cached:
            return cached

        project_meta: dict[str, Any] = await self.__pypi_api_client.get_project_meta(project_name)
        project_meta_serialized: ProjectMeta = ProjectMeta(**project_meta.get("info", {}))
        await self.__pypi_cache_repo.set_project_meta(project_name, project_meta_serialized)

        return project_meta_serialized

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
