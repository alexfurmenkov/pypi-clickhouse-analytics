from collections.abc import Iterable

from pydantic import BaseModel

from pypi_clickhouse_analytics.enums.group_by_enum import GroupByColumn


class ProjectDownloads(BaseModel):
    downloads: int


class GroupedDownloadItem(BaseModel):
    value: str
    downloads: int


class GroupedDownloads(BaseModel):
    grouped_by: GroupByColumn
    items: Iterable[GroupedDownloadItem]
