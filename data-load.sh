#!/bin/bash

docker build -t data-loader ./data-loader/.
echo "Container built!"

docker run \
    --name data-loader \
    --env-file ./.env \
    -v provato-logs-load:/data  \
    --network host \
    data-loader

echo "Container created!"

docker container rm data-loader
echo "Container deleted!"
