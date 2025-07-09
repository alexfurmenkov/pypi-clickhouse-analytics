from typing import Generator

from clickhouse_connect.driver import AsyncClient
from clickhouse_connect.driver.query import QueryResult
from datetime import datetime

from pypi_clickhouse_analytics.enums.group_by_enum import GroupByColumn


class PyPiProjectAnalyticsRepo:
    def __init__(self, clickhouse_client: AsyncClient):
        self.__clickhouse_client = clickhouse_client
        self.__table_name = "pypi"  # TODO mb in config

    async def get_download_count(
        self,
        project_name: str,
        *,
        from_dt: datetime | None = None,
        to_dt: datetime | None = None
    ) -> int:
        where_expressions: list[str] = [f"PROJECT = '{project_name}'"]
        if from_dt:
            where_expressions.append(f"TIMESTAMP >= '{from_dt.isoformat()}'")
        if to_dt:
            where_expressions.append(f"TIMESTAMP <= '{to_dt.isoformat()}'")

        where_stmt: str = " AND ".join(where_expressions)
        query: str = f"""
            SELECT COUNT(PROJECT) 
            FROM {self.__table_name}
            WHERE {where_stmt}
        """

        # TODO use params to avoid injections
        result: QueryResult = await self.__clickhouse_client.query(query)
        count = result.result_rows[0][0]
        return int(count)

    async def group_downloads(
        self,
        project_name: str,
        *,
        group_by_column: GroupByColumn,
        from_dt: datetime | None = None,
        to_dt: datetime | None = None
    ) -> Generator[dict, None, None]:
        where_expressions: list[str] = [f"PROJECT = '{project_name}'"]
        if from_dt:
            where_expressions.append(f"TIMESTAMP >= '{from_dt.isoformat()}'")
        if to_dt:
            where_expressions.append(f"TIMESTAMP <= '{to_dt.isoformat()}'")

        where_stmt: str = " AND ".join(where_expressions)
        group_by_column_upper: str = group_by_column.upper()
        query: str = f"""
            SELECT 
              {group_by_column_upper} AS {group_by_column}, 
              COUNT({group_by_column_upper}) AS DOWNLOAD_COUNT
            FROM {self.__table_name}
            WHERE {where_stmt}
            GROUP BY {group_by_column_upper}
            ORDER BY DOWNLOAD_COUNT
        """
        result: QueryResult = await self.__clickhouse_client.query(query)
        return result.named_results()
