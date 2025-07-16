from collections.abc import Iterable

from pydantic import BaseModel

from pypi_clickhouse_analytics.enums.group_by_enum import GroupByColumn


class ProjectMeta(BaseModel):
    name: str
    author: str
    author_email: str | None = None
    description: str
    home_page: str | None = None
    license: str
    requires_python: str


class ProjectDownloads(BaseModel):
    project: str
    downloads: int


class GroupedDownloadItem(BaseModel):
    value: str
    downloads: int


class GroupedDownloads(BaseModel):
    grouped_by: GroupByColumn
    items: Iterable[GroupedDownloadItem]
