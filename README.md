# PROVATO - Data Loader & Retriever

This repository is part of the PROVATO research project funded by the Agrarian EU Horizon project.

The repository contains three Dockerized scripts that perform the following tasks:
1. [data-loader directory](./data-loader/) – Loads user and animal metadata from the Digitanimal API into a Timescale database.
2. Not ready ❌ – Retrieves short-term (hourly) data provided by Digitanimal devices and injects it into a Timescale database.
3. [data-retrieval directory](./data-retrieval/) – Retrieves long-term data provided by Digitanimal devices and injects it into a Timescale database.

Note: The repository includes a Docker Compose file that creates a database for testing purposes using the Dockerized scripts.

Find more information here about:
- [PROVATO](https://www.linkedin.com/showcase/provatoproject/)
- [Digitanimal Livestock Tracking Devices](https://digitanimal.com/)

## Prerequisites

A machine running Docker CLI version >= 25.0 and Docker Desktop >= 4.4.0 should have no issues running the scripts.

Running the scripts also assumes that a Timescale database is available at `POSTGRES_HOST:POSTGRES_PORT`. Using TimescaleDB version >= 2.19.3 with PostgreSQL version >= 14 should work without issues.

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

Once a Timescale database is available and the environment variables are set up, the containers can be run using the appropriate scripts. Each script creates logs saved in the Git-ignored `data` directory of the project.

1. [data-load.sh](./data-load.sh) – Loads user and animal metadata from the Digitanimal API into a Timescale database.
2. Not ready ❌ – Retrieves short-term data provided by Digitanimal devices and injects it into a Timescale database.
3. [data-retrieval.sh](./data-retrieval.sh) – Retrieves long-term data provided by Digitanimal devices and injects it into a Timescale database.


## Scheduling with Cron

The data retrieval scripts can be added as cron tasks on a machine to inject new data every thirty minutes for the short-term data or every day for the long-term data.

Below are the cron settings. Modify the `PROJECTPATH` to the appropriate path and ensure the user running the tasks has permissions to build, run, and delete Docker containers.

```bash
# Short-term data every 30 minutes
*/30 * * * * cd /path/to/project && /bin/bash ./data-retrieval-short.sh

# Long-term data every day at 9 AM
0 9 * * * cd /path/to/project && /bin/bash ./data-retrieval.sh
```

## Acknowledgements

PROVATO is funded by EU under Horizon Europe, selected by [AGRARIAN 1st open call](https://agrarian-project.eu).
