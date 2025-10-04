DROP TABLE IF EXISTS stations;

--Table to store weather station information
--This is what you get from the stations API endpoint
CREATE TABLE stations (
    station_id   VARCHAR(50) PRIMARY KEY,
    name         TEXT NOT NULL,
    state        VARCHAR(50),
    latitude     DOUBLE PRECISION,
    longitude    DOUBLE PRECISION,
    elevation    DOUBLE PRECISION,
    active       BOOLEAN
);

DROP TABLE IF EXISTS weather_data;
CREATE TABLE weather_data (
    id           SERIAL PRIMARY KEY,
    station_id   VARCHAR(50) REFERENCES stations(station_id),
    timestamp    TIMESTAMP NOT NULL,
    temperature  DOUBLE PRECISION,
);