FROM python:3.11.9

WORKDIR /usr/app

RUN ["mkdir", "-p", "/data"]

COPY requirements.txt requirements.txt

RUN ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]

COPY . .

# Digitanimal related
ENV DIGITANIMAL_USER=user
ENV DIGITANIMAL_PASS=pass

# POSTGRES related
ENV POSTGRES_HOST=127.0.0.1
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=db
ENV POSTGRES_USER=user
ENV POSTGRES_PASS=pass
ENV POSTGRES_TABLE_NAME=DEVICE_DATA

# Other
ENV LAST_YEAR_FLAG=FALSE
ENV TEMP_FOLDER=/data

# Shell run to save output inside the container
ENTRYPOINT ["sh", "-c", "python main.py >> /data/retrieve.logs 2>&1"]
