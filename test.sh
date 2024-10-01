#!/bin/bash

upload_response=$(curl -s -X POST "http://127.0.0.1:8000/upload-csv/" -F "file=@data.csv")

file_id=$(echo $upload_response | jq -r '.file_id')
headers=$(echo $upload_response | jq -r '.headers')
map_layer=$(echo $upload_response | jq -r '.map_layer')
if [ -z "$file_id" ] || [ "$file_id" == "null" ]; then
  echo "Error: Failed to extract file_id"
  exit 1
fi

echo "File ID: $file_id"
echo "Headers: $headers"
echo "Map Layer: $map_layer"

csv_response=$(curl -s "http://127.0.0.1:8000/csv/$file_id?page=1&rows_per_page=2")
echo "Paginated CSV (Page 1, 2 rows per page):"
echo "$csv_response" | jq .

map_layer_response=$(curl -s -X POST "http://127.0.0.1:8000/map-layer/$file_id?identifier_column=name")

echo "Map Layer Response:"
echo "$map_layer_response" | jq .
