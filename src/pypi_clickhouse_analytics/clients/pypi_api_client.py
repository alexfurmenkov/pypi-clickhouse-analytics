from typing import Any

from httpx import AsyncClient, Request, Response
from starlette import status

from pypi_clickhouse_analytics.app_settings import settings
from pypi_clickhouse_analytics.exceptions.resource import NotFoundError
from pypi_clickhouse_analytics.exceptions.service import DownstreamServiceUnavailable


class PyPiAPIClient:
    def __init__(
        self, http_client: AsyncClient, pypi_api_url: str = settings.PYPI_API_URL
    ) -> None:
        self._http_client = http_client
        self.__pypi_api_url = pypi_api_url

    async def get_project_meta(self, project_name: str) -> dict[str, Any]:
        response: Response = await self.__send(
            Request(
                url=f"{self.__pypi_api_url}/{project_name}/json",
                method="GET",
            )
        )
        return response.json()

    async def __send(self, request: Request) -> Response:
        response: Response = await self._http_client.send(request)
        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise NotFoundError("Resource not found")
        if response.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
            raise DownstreamServiceUnavailable("PyPi API is unavailable")
        return response
