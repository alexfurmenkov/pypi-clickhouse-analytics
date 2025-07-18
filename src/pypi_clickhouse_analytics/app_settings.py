from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    This class defines app settings that can be overwritten with env vars.
    """

    CLICKHOUSE_HOST: str = "localhost"
    CLICKHOUSE_PORT: int = 8123
    CLICKHOUSE_USER: str
    CLICKHOUSE_PASS: str
    CLICKHOUSE_DB: str = "default"
    HTTPX_TIMEOUT: int = 60

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_USERNAME: str | None = None
    REDIS_PASSWORD: str | None = None

    PROJECT_META_CACHE_TTL_HOURS: int = 2

    PYPI_API_URL: str = "https://pypi.org/pypi"
    PYPI_DATASET_URL: str = "https://datasets-documentation.s3.eu-west-3.amazonaws.com/pypi/2023/pypi_0_7_34.snappy.parquet"

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
