from typing import Any

from httpx import Response, Request, AsyncClient

from pypi_clickhouse_analytics.app_settings import settings


class PyPiAPIClient:
    def __init__(self, http_client: AsyncClient, pypi_api_url: str = settings.PYPI_API_URL):
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
        # TODO log and raise if bad response
        return response
