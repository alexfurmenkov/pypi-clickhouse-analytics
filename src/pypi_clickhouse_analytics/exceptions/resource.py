from pypi_clickhouse_analytics.exceptions.base import BaseError


class NotFoundError(BaseError):
    status_code = 404
