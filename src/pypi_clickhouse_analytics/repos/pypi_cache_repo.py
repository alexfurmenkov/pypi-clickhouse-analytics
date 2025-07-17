from datetime import timedelta

from pypi_clickhouse_analytics.app_settings import settings
from pypi_clickhouse_analytics.clients import CacheClient
from pypi_clickhouse_analytics.entities.projects import ProjectMeta


class PypiCacheRepo:
    def __init__(self, cache: CacheClient) -> None:
        self.__cache = cache

    async def get_project_meta(self, project_name: str) -> ProjectMeta | None:
        project_meta: dict | None = await self.__cache.get(
            self.__project_meta_cache_key(project_name)
        )
        if project_meta is not None:
            return ProjectMeta.model_validate(project_meta)

    async def set_project_meta(
        self, project_name: str, project_meta: ProjectMeta
    ) -> None:
        await self.__cache.set(
            self.__project_meta_cache_key(project_name),
            project_meta,
            ttl=timedelta(hours=settings.PROJECT_META_CACHE_TTL_HOURS),
        )

    def __project_meta_cache_key(self, project_name: str) -> str:
        return f"{project_name}_meta"
