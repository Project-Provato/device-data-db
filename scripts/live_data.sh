#!/bin/bash

docker build --no-cache -t data-retrieval ./live_data_load/.
echo "Container built!"

docker run --rm \
    --name data-retrieval \
    --env-file ./.env \
    -v provato-logs-retrieve:/data  \
    --network host \
    data-retrieval

echo "Container run!"
