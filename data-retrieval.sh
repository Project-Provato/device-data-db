#!/bin/bash

mkdir -p ./data

docker build -t data-retrieval ./data-retrieval/.
echo "Container built!"

docker run --name data-retrieval --env-file ./.env data-retrieval >> ./data/retrieval.log 2>&1
echo "Container created!"

docker container rm data-retrieval
echo "Container deleted!"
