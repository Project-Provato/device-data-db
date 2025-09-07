#!/bin/bash

docker build --no-cache -t data-loader ./init_data_load/.
echo "Container built!"

docker run --rm \
    --name data-loader \
    --env-file ./.env \
    -v provato-logs-load:/data  \
    --network host \
    data-loader

echo "Container run!"
