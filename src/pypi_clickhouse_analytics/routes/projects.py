from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.params import Depends

from pypi_clickhouse_analytics.dependencies.services import get_pypi_analytics_service
from pypi_clickhouse_analytics.enums.group_by_enum import GroupByColumn
from pypi_clickhouse_analytics.services.pypi_analytics_service import PyPiAnalyticsService

router = APIRouter()

@router.get("/{project_name}")
async def get_project(
    project_name: str,
    *,
    analytics_service: Annotated[PyPiAnalyticsService, Depends(get_pypi_analytics_service)],
):
    return await analytics_service.get_project_meta(project_name)


@router.get("/{project_name}/downloads")
async def get_project_downloads(
    project_name: str,
    *,
    start_date: Annotated[datetime | None, Query(alias="startDate")] = None,
    end_date: Annotated[datetime | None, Query(alias="endDate")] = None,
    analytics_service: Annotated[PyPiAnalyticsService, Depends(get_pypi_analytics_service)],
):
    return await analytics_service.get_project_download_count(project_name, from_dt=start_date, to_dt=end_date)


@router.get("/{project_name}/downloads/{group_by_column}")
async def group_project_downloads(
    project_name: str,
    group_by_column: GroupByColumn,
    *,
    start_date: Annotated[datetime | None, Query(alias="startDate")] = None,
    end_date: Annotated[datetime | None, Query(alias="endDate")] = None,
    analytics_service: Annotated[PyPiAnalyticsService, Depends(get_pypi_analytics_service)],
):
    return await analytics_service.group_project_downloads(
        project_name, group_by_column, from_dt=start_date, to_dt=end_date
    )
