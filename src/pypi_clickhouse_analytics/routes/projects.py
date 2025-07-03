from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/{project_name}")
async def get_project(project_name: str):
    pass


@router.get("/{project_name}/downloads")
async def get_project_downloads(
    project_name: str,
    *,
    start_date: Annotated[datetime | None, Query(alias="startDate")] = None,
    end_date: Annotated[datetime | None, Query(alias="endDate")] = None,
):
    pass


@router.get("/{project_name}/countries")
async def get_project_countries(
    project_name: str,
    *,
    start_date: Annotated[datetime | None, Query(alias="startDate")] = None,
    end_date: Annotated[datetime | None, Query(alias="endDate")] = None,
):
    pass


@router.get("/{project_name}/python-versions")
async def get_project_python_versions(
    project_name: str,
    *,
    start_date: Annotated[datetime | None, Query(alias="startDate")] = None,
    end_date: Annotated[datetime | None, Query(alias="endDate")] = None,
):
    pass
