
DROP TABLE s_delta.recordings
DROP TABLE s_delta.plant
DROP TABLE s_delta.origin
DROP TABLE s_delta.botanist


CREATE TABLE s_delta.botanist(
    botanist_id INT IDENTITY(1, 1) PRIMARY KEY,
    first_name varchar(25) NOT NULL,
    last_name varchar(30) NOT NULL,
    email varchar(320) NOT NULL,
    phone_num varchar(20) NOT NULL
);
GO

CREATE TABLE s_delta.origin(
    origin_id INT IDENTITY(1, 1) PRIMARY KEY,
    area varchar(50) NOT NULL,
    longitude float NOT NULL,
    latitude float NOT NULL
);
GO

CREATE TABLE s_delta.plant(
    plant_id INT PRIMARY KEY,
    common_name varchar(50) NOT NULL,
    scientific_name varchar(50),
    origin_id INT NOT NULL,
    FOREIGN KEY (origin_id) REFERENCES s_delta.origin(origin_id)
);
GO

CREATE TABLE s_delta.recordings(
    recording_id bigint IDENTITY(1, 1) PRIMARY KEY,
    recording_taken DATETIME NOT NULL,
    last_watered DATETIME NOT NULL,
    soil_moisture float NOT NULL,
    temperature float NOT NULL,
    plant_id INT NOT NULL,
    botanist_id INT NOT NULL,
    FOREIGN KEY (plant_id) REFERENCES s_delta.plant(plant_id),
    FOREIGN KEY (botanist_id) REFERENCES s_delta.botanist(botanist_id)
);
GO

