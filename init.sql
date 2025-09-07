-- CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE FARMS_API (
    id serial PRIMARY KEY,
    id_api int UNIQUE NOT NULL,
    name char(100),
    coordinates polygon
);

CREATE TABLE ANIMALS_API (
    id serial PRIMARY KEY,
    id_api char(5) UNIQUE NOT NULL,
    name char(100),
    date_birth date,
    type char(100),
    sex char(100),
    breed char(100),
    breed_short char(100),
    farm_id_api int,
    farm_id int,
    FOREIGN KEY (farm_id_api) REFERENCES FARMS_API(id_api)
);

CREATE TABLE DEVICES_API (
    id serial PRIMARY KEY,
    id_api char(5) UNIQUE NOT NULL,
    type char(100),
    FOREIGN KEY (id_api) REFERENCES ANIMALS_API(id_api)
);

CREATE TABLE DEVICE_DATA_API (
    id serial,
    id_api char(5),
    created_at timestamp,
    pos_x real,
    pos_y real,
    pos_z real,
    std_x real,
    std_y real,
    std_z real,
    max_x real,
    max_y real,
    max_z real,
    temperature real,
    coordinates point,
    FOREIGN KEY (id_api) REFERENCES DEVICES_API(id_api)
);

CREATE TABLE DEVICE_DATA_SEVEN_API (
  id 					serial,
  id_api 				char(5),
  created_at 			timestamp,
  coordinates 			point,
  raw_acc_x 			real,
  raw_acc_y 			real,
  raw_acc_z 			real,
  temperature 			real,
  flag_alarm 			smallint,
  flag_temperature 		smallint,
  flag_distance 		smallint,
  flag_activity 		smallint,
  flag_position 		smallint,
  flag_outside_farm 	smallint,
  temperature_current 	real,
  temperature_weekly 	real,
  temperature_herd 		real,
  activity_current 		real,
  activity_weekly 		real,
  activity_herd 		real,
  distance_current 		real,
  distance_weekly 		real,
  distance_herd 		real,
  FOREIGN KEY (id_api) REFERENCES DEVICES_API(id_api)
);

ALTER TABLE DEVICE_DATA_API ADD PRIMARY KEY (id_api, created_at);
ALTER TABLE DEVICE_DATA_SEVEN_API ADD PRIMARY KEY (id_api, created_at);

-- CREATE INDEX index_device_data_collar ON DEVICE_DATA(id_collar);

-- SELECT create_hypertable('device_data', 'created_at');
