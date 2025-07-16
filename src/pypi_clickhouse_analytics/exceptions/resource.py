from starlette import status

from pypi_clickhouse_analytics.exceptions.base import BaseError


class NotFoundError(BaseError):
    status_code = status.HTTP_404_NOT_FOUND
