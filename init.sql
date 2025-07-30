-- for unique UUID and not auto-increment
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS timescaledb;


-- initializing tables...

CREATE TABLE USERS (
    id INT PRIMARY KEY NOT NULL,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    password_hash TEXT
);

-- INSERT INTO USERS(id, first_name, last_name, email, password_hash) VALUES (1, '', '', '', '');

CREATE TABLE ANIMALS (
    id CHARACTER(5) PRIMARY KEY NOT NULL,
    animal_name TEXT,
    date_birth TIMESTAMPTZ,
    genus TEXT,
    sex TEXT,
    breed TEXT,
    breed_short CHARACTER(3),
    id_farm INT
    -- CONSTRAINT fk_parent FOREIGN KEY (id_farm) REFERENCES FARMS(id) ON DELETE SET NULL
);

CREATE TABLE FARMS (
    id INT PRIMARY KEY NOT NULL,
    farm_name TEXT,
    area REAL,
    coordinates polygon,
    id_user INT
    -- CONSTRAINT fk_parent FOREIGN KEY (id_user) REFERENCES USERS(id) ON DELETE SET NULL
);

-- INSERT INTO FARMS(id, farm_name, area, coordinates, id_user) VALUES (0, '', 0, '', 1);

CREATE TABLE DEVICE_DATA (
    id UUID DEFAULT uuid_generate_v4(),
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
    coordinates POINT
    -- CONSTRAINT fk_parent FOREIGN KEY (id_collar) REFERENCES DEVICES(id) ON DELETE SET NULL
);

ALTER TABLE device_data ADD PRIMARY KEY (id_collar, created_at);
CREATE INDEX index_device_data_collar ON DEVICE_DATA(id_collar);

SELECT create_hypertable('device_data', 'created_at');
