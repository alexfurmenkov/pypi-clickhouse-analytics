from pydantic import BaseModel


class ProjectDownloads(BaseModel):
    downloads: int
