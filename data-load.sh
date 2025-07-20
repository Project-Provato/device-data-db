#!/bin/bash

mkdir -p ./data

docker build -t data-loader ./data-loader/.
echo "Container built!"

docker run --name data-loader --env-file ./.env data-loader >> ./data/loader.log 2>&1
echo "Container created!"

docker container rm data-loader
echo "Container deleted!"
