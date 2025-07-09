from clickhouse_connect.driver import AsyncClient
from clickhouse_connect.driver.query import QueryResult
from datetime import datetime


class PyPiAnalyticsRepo:
    def __init__(self, clickhouse_client: AsyncClient):
        self.__clickhouse_client = clickhouse_client
        self.__table_name = "pypi"  # TODO mb in config

    async def get_project_download_count(
        self,
        project_name: str,
        from_dt: datetime | None = None,
        to_dt: datetime | None = None
    ) -> int:
        where_expressions: list[str] = [f"PROJECT = '{project_name}'"]
        if from_dt:
            where_expressions.append(f"TIMESTAMP >= '{from_dt.isoformat()}'")
        if to_dt:
            where_expressions.append(f"TIMESTAMP <= '{to_dt.isoformat()}'")

        where_stmt: str = " AND ".join(where_expressions)
        query = f"""
            SELECT COUNT(PROJECT) 
            FROM {self.__table_name}
            WHERE {where_stmt}
        """

        # TODO use params to avoid injections
        result: QueryResult = await self.__clickhouse_client.query(query)
        count = result.result_rows[0][0]
        return int(count)
