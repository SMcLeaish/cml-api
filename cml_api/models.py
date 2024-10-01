from typing import Optional
from pydantic import BaseModel, Field


class PaginatedCSV(BaseModel):
    headers: list[str]
    total_rows: int
    data: list[list[str]]
    page: int
    rows_per_page: int


class CSVUploadResponse(BaseModel):
    file_id: str
    headers: list[str]
    map_layer: bool


class MapPoint(BaseModel):
    latitude: float = Field(
        ..., ge=-90, le=90, description="Latitude must be between -90 and 90"
    )
    longitude: float = Field(
        ..., ge=-180, le=180, description="Longitude must be between -180 and 180"
    )
    mgrs: str
    identifier: Optional[str] = None


class MapLayer(BaseModel):
    points: list[MapPoint]
