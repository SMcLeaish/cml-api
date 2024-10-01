from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from typing import Optional, Dict
import csv
import uuid
from io import StringIO
from cml_api.models import MapPoint, MapLayer, PaginatedCSV, CSVUploadResponse

app: FastAPI = FastAPI()

csv_storage: Dict[str, str] = {}
map_layers_storage: Dict[str, MapLayer] = {}


@app.post("/upload-csv/", response_model=CSVUploadResponse)
async def upload_csv(file: UploadFile = File(...)) -> CSVUploadResponse:
    content: bytes = await file.read()
    decoded_content: str = content.decode("utf-8")
    file_id: str = str(uuid.uuid4())
    csv_storage[file_id] = decoded_content

    reader = csv.reader(StringIO(decoded_content))
    headers: list[str] = next(reader)

    lat_col: Optional[str] = "latitude" if "latitude" in headers else None
    long_col: Optional[str] = "longitude" if "longitude" in headers else None

    if lat_col and long_col:
        lat_idx: int = headers.index(lat_col)
        long_idx: int = headers.index(long_col)

        map_points: list[MapPoint] = []
        for row in reader:
            try:
                point = MapPoint(
                    latitude=float(row[lat_idx]),
                    longitude=float(row[long_idx]),
                    mgrs="",
                    identifier=None,
                )
                map_points.append(point)
            except (ValueError, HTTPException):
                continue

        if map_points:
            map_layers_storage[file_id] = MapLayer(points=map_points)
            return CSVUploadResponse(file_id=file_id, headers=headers, map_layer=True)

    return CSVUploadResponse(file_id=file_id, headers=headers, map_layer=False)


@app.get("/csv/{file_id}", response_model=PaginatedCSV)
async def view_csv(
    file_id: str, page: int = Query(1, ge=1), rows_per_page: int = Query(10, ge=1)
) -> PaginatedCSV:
    csv_content: Optional[str] = csv_storage.get(file_id)
    if csv_content is None:
        raise HTTPException(status_code=404, detail="File not found")

    reader = csv.reader(StringIO(csv_content))
    headers: list[str] = next(reader)

    paginated_rows: list[list[str]] = []
    start_row: int = (page - 1) * rows_per_page
    end_row: int = start_row + rows_per_page

    for i, row in enumerate(reader):
        if start_row <= i < end_row:
            paginated_rows.append(row)
        if i >= end_row:
            break

    total_rows: int = i + 1

    return PaginatedCSV(
        headers=headers,
        data=paginated_rows,
        total_rows=total_rows,
        page=page,
        rows_per_page=rows_per_page,
    )


@app.post("/map-layer/{file_id}")
async def create_map_layer_with_identifier(
    file_id: str, identifier_column: str
) -> dict[str, list[MapPoint]]:
    map_layer: Optional[MapLayer] = map_layers_storage.get(file_id)
    if map_layer is None:
        raise HTTPException(status_code=404, detail="Map layer not found")

    csv_content: Optional[str] = csv_storage.get(file_id)
    if csv_content is None:
        raise HTTPException(status_code=404, detail="File not found")

    reader = csv.reader(StringIO(csv_content))
    headers: list[str] = next(reader)

    if identifier_column not in headers:
        raise HTTPException(status_code=400, detail="Invalid identifier column")

    identifier_idx: int = headers.index(identifier_column)

    for i, row in enumerate(reader):
        if i < len(map_layer.points):
            map_layer.points[i].identifier = row[identifier_idx]

    return {"map_layer": map_layer.points}
