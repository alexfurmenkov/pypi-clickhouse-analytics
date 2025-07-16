from datetime import datetime
from typing import Annotated, Iterable

from fastapi import APIRouter, Query
from fastapi.params import Depends
from starlette import status

from pypi_clickhouse_analytics.dependencies.services import get_pypi_analytics_service
from pypi_clickhouse_analytics.entities.projects import ProjectMeta, ProjectDownloads, GroupedDownloads
from pypi_clickhouse_analytics.enums import GroupByColumn
from pypi_clickhouse_analytics.services import PyPiAnalyticsService

router = APIRouter()

@router.get(
    "/{project_name}",
    response_model=ProjectMeta,
    status_code=status.HTTP_200_OK,
)
async def get_project(
    project_name: str,
    *,
    analytics_service: Annotated[PyPiAnalyticsService, Depends(get_pypi_analytics_service)],
):
    return await analytics_service.get_project_meta(project_name)


@router.get(
    "/{project_name}/downloads",
    response_model=ProjectDownloads,
    status_code=status.HTTP_200_OK,
)
async def get_project_downloads(
    project_name: str,
    *,
    start_date: Annotated[datetime | None, Query] = None,
    end_date: Annotated[datetime | None, Query] = None,
    analytics_service: Annotated[PyPiAnalyticsService, Depends(get_pypi_analytics_service)],
):
    return await analytics_service.get_project_download_count(project_name, from_dt=start_date, to_dt=end_date)


@router.get(
    "/{project_name}/downloads/{group_by_column}",
    response_model=GroupedDownloads,
    status_code=status.HTTP_200_OK,
)
async def group_project_downloads(
    project_name: str,
    group_by_column: GroupByColumn,
    *,
    start_date: Annotated[datetime | None, Query] = None,
    end_date: Annotated[datetime | None, Query] = None,
    analytics_service: Annotated[PyPiAnalyticsService, Depends(get_pypi_analytics_service)],
):
    return await analytics_service.group_project_downloads(
        project_name, group_by_column, from_dt=start_date, to_dt=end_date
    )


@router.get(
    "/downloads/top",
    response_model=Iterable[ProjectDownloads],
    status_code=status.HTTP_200_OK,
)
async def list_most_downloaded_projects(
    analytics_service: Annotated[PyPiAnalyticsService, Depends(get_pypi_analytics_service)],
    start_date: Annotated[datetime | None, Query] = None,
    end_date: Annotated[datetime | None, Query] = None,
    limit: Annotated[int | None, Query] = 50,
):
    return await analytics_service.list_most_downloaded_projects(start_date, end_date, limit)
