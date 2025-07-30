#!/bin/bash

docker build -t data-retrieval ./data-retrieval/.
echo "Container built!"

docker run \
    --name data-retrieval \
    --env-file ./.env \
    -v provato-logs-retrieve:/data  \
    --network host \
    data-retrieval

echo "Container created!"

docker container rm data-retrieval
echo "Container deleted!"
