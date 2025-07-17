from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import Response

from pypi_clickhouse_analytics.exceptions.base import BaseError
from pypi_clickhouse_analytics.routes import projects

app = FastAPI()
app.include_router(projects.router, prefix="/projects", tags=["Projects"])


@app.exception_handler(BaseError)
async def base_service_error_handler(request: Request, exc: BaseError) -> Response:
    return await http_exception_handler(
        request,
        HTTPException(
            status_code=exc.status_code,
            detail=exc.args[0],
        ),
    )


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception) -> Response:
    return await http_exception_handler(
        request, HTTPException(status_code=500, detail="Internal Server Error")
    )
