# ruff: noqa: S608
import asyncio

from clickhouse_connect.driver import AsyncClient as AsyncClickHouseClient

from pypi_clickhouse_analytics.app_settings import settings
from pypi_clickhouse_analytics.dependencies.clients import get_clickhouse_client


async def load_dataset_into_clickhouse() -> None:
    clickhouse_client: AsyncClickHouseClient = await get_clickhouse_client()
    await clickhouse_client.query("""
        CREATE TABLE IF NOT EXISTS pypi (
            TIMESTAMP DateTime,
            COUNTRY_CODE String,
            URL String,
            PROJECT String,
            PYTHON String
        )
        ENGINE = MergeTree
        PRIMARY KEY (PROJECT, TIMESTAMP);
    """)

    result = await clickhouse_client.query("SELECT count() FROM pypi")
    count = result.result_rows[0][0]
    if count > 0:
        print(f"Table already populated with {count} rows. Skipping load.")
        return

    print("Inserting data into pypi from S3...")

    await clickhouse_client.query(f"""
        INSERT INTO pypi
        SELECT 
          TIMESTAMP, 
          COUNTRY_CODE, 
          URL, 
          PROJECT, 
          PYTHON 
        FROM s3(
            '{settings.PYPI_DATASET_URL}'
        );
    """)

    print("Data inserted successfully.")


def main() -> None:
    asyncio.run(load_dataset_into_clickhouse())
