from fastapi import FastAPI

from pypi_clickhouse_analytics.routes import projects

app = FastAPI()
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
