import csv
import uuid
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from io import StringIO
from typing import Optional
from .models import PaginatedCSV

app = FastAPI()

csv_storage = {}


@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    content = await file.read()
    decoded_content = content.decode("utf-8")
    file_id = str(uuid.uuid4())
    csv_storage[file_id] = decoded_content

    reader = csv.reader(StringIO(decoded_content))
    headers = next(reader)
    return {"file_id": file_id, "headers": headers}


@app.get("/get-csv/{file_id}", response_model=PaginatedCSV)
async def get_csv(
    file_id: str, page: int = Query(1, ge=1), rows_per_page: int = Query(10, ge=1)
):
    csv_content: Optional[str] = csv_storage.get(file_id)

    if csv_content is None:
        raise HTTPException(status_code=404, detail="File not found")
    reader = csv.reader(StringIO(csv_content))
    headers = next(reader)

    start_row = (page - 1) * rows_per_page
    end_row = start_row + rows_per_page

    paginated_rows: list[list[str]] = []

    i = -1

    for i, row in enumerate(reader):
        if start_row <= i < end_row:
            paginated_rows.append(row)
        if i >= end_row:
            break

    return PaginatedCSV(
        headers=headers,
        data=paginated_rows,
        total_rows=i + 1,
        page=page,
        rows_per_page=rows_per_page,
    )
