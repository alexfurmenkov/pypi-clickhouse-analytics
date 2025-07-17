from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    This class defines app settings that can be overwritten with env vars.
    """

    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int
    CLICKHOUSE_USER: str
    CLICKHOUSE_PASS: str
    CLICKHOUSE_DB: str
    PYPI_API_URL: str = "https://pypi.org/pypi"
    HTTPX_TIMEOUT: int = 60

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_USERNAME: str | None = None
    REDIS_PASSWORD: str | None = None

    PROJECT_META_CACHE_TTL_HOURS: int = 2

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
