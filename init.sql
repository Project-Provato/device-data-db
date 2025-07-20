-- for unique UUID and not auto-increment
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS timescaledb;


-- initializing tables...

CREATE TABLE USERS (
    id INT PRIMARY KEY NOT NULL,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    password_hash TEXT NOT NULL
);

CREATE TABLE DEVICE_DATA (
    id UUID DEFAULT uuid_generate_v4(),
    -- id_user_datanimal INT,
    -- id_user INT,
    id_collar CHARACTER(5),
    created_at TIMESTAMPTZ NOT NULL,
    pos_x REAL,
    pos_y REAL,
    pos_z REAL,
    std_x REAL,
    std_y REAL,
    std_z REAL,
    max_x REAL,
    max_y REAL,
    max_z REAL,
    temperature REAL,
    longitude DOUBLE PRECISION,
    latitude DOUBLE PRECISION
    -- CONSTRAINT fk_parent FOREIGN KEY (id_user) REFERENCES USERS(id) ON DELETE SET NULL,
    -- CONSTRAINT fk_parent FOREIGN KEY (id_collar) REFERENCES DEVICES(id) ON DELETE SET NULL
);

ALTER TABLE device_data ADD PRIMARY KEY (id_collar, created_at);
CREATE INDEX index_device_data_collar ON DEVICE_DATA(id_collar);

SELECT create_hypertable('device_data', 'created_at');
