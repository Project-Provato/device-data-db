# PROVATO - Data Loader & Retriever

This repository is part of the PROVATO research project funded by the Agrarian EU Horizon project.

The repository contains two Dockerized scripts that perform the following tasks:
1. [init_data_load directory](./init_data_load/) – Loads farms, animals and devices from the Digitanimal API into a Postgres database.
2. [live_data_load directory](./live_data_load/) – Retrieves long-term data provided by Digitanimal devices and injects it into a Postgres database. This data is filtered by Digitanimal, keeping only valid data throughout the day. Only data up to 1 day ago can be retrieved.

Note: The repository includes a Docker Compose file that creates a database for testing purposes using the Dockerized scripts.

Find more information here about:
- [Research Project PROVATO](https://www.linkedin.com/showcase/provatoproject/)
- [Digitanimal Livestock Tracking Devices](https://digitanimal.com/)

## Prerequisites

A machine running Docker CLI version >= 25.0 and Docker Desktop >= 4.4.0 should have no issues running the scripts.

Running the scripts also assumes that a Postgres database is available at `POSTGRES_HOST:POSTGRES_PORT`. Using PostgreSQL version >= 14 should work without issues.

### Environment Variables ❗

Before proceeding, a `.env` file must be created based on the [.envsample](./.envsample) file, as these variables are required to run the scripts.

### Functionality Testing – Dummy TimescaleDB

If no Timescale database is available and the functionality of the scripts is being tested, the Compose file can be run:

```bash
docker compose up -d
```

This will create a Timescale database using the schema defined by [init.sql](./init.sql). An Adminer container is also set up to provide a web interface for accessing this database.

To destroy the compose containers run:

```bash
docker compose down
```

## How to Run

Once a Timescale database is available and the environment variables are set up, the containers can be run using the appropriate scripts. 
1. [init_data.sh](./scripts/init_data.sh) – Loads farms, animals and devices from the Digitanimal API into a Postgres database.
2. [live_Data.sh](./scripts/live_data.sh) – Retrieves long-term data provided by Digitanimal devices and injects it into a Postgres database.

❗**Before running the scripts** two docker volumes need to be created that will save the logs of the python scritps.

```bash
docker volume create provato-logs-retrieve
docker volume create provato-logs-load
```

## Scheduling with Cron

The data retrieval scripts can be added as cron tasks on a machine to inject new data every thirty minutes for the short-term data or every day for the long-term data.

Below are the cron settings. Modify the project path to the appropriate path and ensure the user running the tasks has permissions to build, run, and delete Docker containers.

```bash
# Long-term data every day at 9 AM
0 9 * * * cd /path/to/project && /bin/bash ./data-retrieval.sh
```

## Acknowledgements

PROVATO is funded by EU under Horizon Europe, selected by [AGRARIAN 1st open call](https://agrarian-project.eu).
