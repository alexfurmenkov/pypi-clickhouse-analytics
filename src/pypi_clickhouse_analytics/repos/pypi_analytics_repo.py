from typing import Generator

from clickhouse_connect.driver import AsyncClient
from clickhouse_connect.driver.query import QueryResult
from datetime import datetime

from pypi_clickhouse_analytics.enums import GroupByColumn


class PyPiProjectAnalyticsRepo:
    def __init__(self, clickhouse_client: AsyncClient):
        self.__clickhouse_client = clickhouse_client
        self.__table_name = "pypi"

    async def get_download_count(
        self,
        project_name: str,
        *,
        from_dt: datetime | None = None,
        to_dt: datetime | None = None
    ) -> int:
        where_statements, params = self.__build_where_statements(project_name=project_name, from_dt=from_dt, to_dt=to_dt)
        where_stmt: str = " AND ".join(where_statements)
        query: str = f"""
            SELECT COUNT(PROJECT) 
            FROM {self.__table_name}
            WHERE {where_stmt}
        """

        result: QueryResult = await self.__clickhouse_client.query(query, parameters=params)
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
        where_statements, params = self.__build_where_statements(project_name=project_name, from_dt=from_dt, to_dt=to_dt)
        where_stmt: str = " AND ".join(where_statements)
        group_by_column_upper: str = group_by_column.upper()
        query: str = f"""
            SELECT 
              {group_by_column_upper} AS {group_by_column}, 
              COUNT({group_by_column_upper}) AS DOWNLOAD_COUNT
            FROM {self.__table_name}
            WHERE {where_stmt}
            GROUP BY {group_by_column_upper}
            ORDER BY DOWNLOAD_COUNT DESC
        """
        result: QueryResult = await self.__clickhouse_client.query(query, parameters=params)
        return result.named_results()

    async def list_most_downloaded_projects(
        self,
        from_dt: datetime | None = None,
        to_dt: datetime | None = None,
        limit: int | None = None
    ) -> Generator[dict, None, None]:
        where_statements, params = self.__build_where_statements(from_dt=from_dt, to_dt=to_dt)
        where_stmt = f"WHERE {' AND '.join(where_statements)}" if where_statements else ""
        query = f"""
            SELECT 
              PROJECT, 
              COUNT(PROJECT) AS DOWNLOAD_COUNT
            FROM {self.__table_name}
            {where_stmt}
            GROUP BY PROJECT
            ORDER BY DOWNLOAD_COUNT DESC
        """
        if limit is not None:
            query += f" LIMIT {limit}"
        result: QueryResult = await self.__clickhouse_client.query(query, parameters=params)
        return result.named_results()

    def __build_where_statements(
        self,
        *,
        project_name: str | None = None,
        from_dt: datetime | None = None,
        to_dt: datetime | None = None
    ) -> tuple[list[str], dict[str, str]]:
        where_stmts: list[str] = []
        params: dict[str, str] = {}
        if project_name:
            where_stmts.append("PROJECT = %(project)s")
            params["project"] = project_name
        if from_dt:
            where_stmts.append("TIMESTAMP >= %(from_dt)s")
            params["from_dt"] = from_dt
        if to_dt:
            where_stmts.append("TIMESTAMP <= %(to_dt)s")
            params["to_dt"] = to_dt

        return where_stmts, params
