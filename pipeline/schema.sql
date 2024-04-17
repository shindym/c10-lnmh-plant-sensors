
DROP TABLE s_delta.recordings
DROP TABLE s_delta.plant
DROP TABLE s_delta.origin
DROP TABLE s_delta.botanist

-- table definitions for the database.
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
    scientific_name varchar(50) DEFAULT NULL,
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

-- Seeding the database.
INSERT INTO s_delta.botanist(first_name,last_name,email,phone_num) VALUES ('Carl','Linnaeus','carl.linnaeus@lnhm.co.uk','(146)994-1635x35992'),
('Gertrude','Jekyll','gertrude.jekyll@lnhm.co.uk','001-481-273-3691x127'),
('Eliza','Andrews','eliza.andrews@lnhm.co.uk','(846)669-6651x75948');
GO

INSERT INTO s_delta.origin(area,longitude,latitude) VALUES ('Resplendor',-19.32556,-41.25528),('Efon-Alaaye',7.65649,4.92235),
('Ilopango',13.70167,-89.10944),('Jashpurnagar',22.88783,84.13864),('Markham',43.86682,-79.2663),('Bonoua',5.27247,-3.59625),('Weimar',50.9803,11.32903),('Kahului',20.88953,-156.47432),('Longview',32.5007,-94.74049),
('Bensheim',49.68369,8.61839),('Gainesville',29.65163,-82.32483),('Siliana',36.08497,9.37082),('Yonkers',40.93121,-73.89875),('Wangon',-7.51611,109.05389),('Oschatz',51.30001,13.10984),('Tonota',-21.44236,27.46153),('Reus',41.15612,1.10687),('Carlos Barbosa',-29.2975,-51.50361)
,('Friedberg',48.35693,10.98461),('Charlottenburg-Nord',52.53048,13.29371),('Motomachi',43.82634,144.09638),('Ar Ruseris',11.8659,34.3869),('El Achir',36.06386,4.62744),('Hlukhiv',51.67822,33.9162),
('Brunswick',43.91452,-69.96533),('Ueno-ebisumachi',34.75856,136.13108),('Ajdabiya',30.75545,20.22625),('Licheng',23.29549,113.82465),('Gifhorn',52.47774,10.5511),('Bachhraon',28.92694,78.23456),
('La Ligua',-32.45242,-71.23106),('Dublin',32.54044,-82.90375),('Malaut',30.21121,74.4818),('Magomeni',-6.8,39.25),('Fujioka',36.24624,139.07204),('Valence',44.92801,4.8951),('Zacoalco de Torres',20.22816,-103.5687),('South Whittier',33.95015,-118.03917),('Salima',-13.7804,34.4587),('Catania',37.49223,15.07041),('Calauan',14.14989,121.3152),
('Acayucan',17.94979,-94.91386);
GO

INSERT INTO s_delta.plant(plant_id,common_name,scientific_name,origin_id) VALUES 
(0,'Epipremnum Aureum','Epipremnum aureum',1),(5,'Pitcher plant','Sarracenia catesbaei',4),(6,'Wollemi pine','Wollemia nobilis',5),
(8,'Bird of paradise','Heliconia schiedeana "Fire and Ice"',6),(9,'Cactus','Pereskia grandifolia',7),(11,'Asclepias Curassavica','Asclepias curassavica',8),
(14,'Colocasia Esculenta','Colocasia esculenta',11),(17,'Ipomoea Batatas','Ipomoea batatas',14),(19,'Musa Basjoo','Musa basjoo',16),(20,'Salvia Splendens','Salvia splendens',17),
(21,'Anthurium','Anthurium andraeanum',18),(22,'Bird of Paradise','Heliconia schiedeana "Fire and Ice"',19),(23,'Cordyline Fruticosa','Cordyline fruticosa',20),
(24,'Ficus','Ficus carica',21),(26,'Dieffenbachia Seguine','Dieffenbachia seguine',23),(27,'Spathiphyllum','Spathiphyllum (group)',24),(28,'Croton','Codiaeum variegatum',25),
(29,'Aloe Vera','Ueno-ebisumachi',26),(30,'Ficus Elastica','Ajdabiya',27),(31,'Sansevieria Trifasciata','Sansevieria trifasciata',28),(32,'Philodendron Hederaceum','Philodendron hederaceum',29),
(33,'Schefflera Arboricola','Schefflera arboricola',30),(34,'Aglaonema Commutatum','Aglaonema commutatum',17),(35,'Monstera Deliciosa','Monstera deliciosa',31),
(36,'Tacca Integrifolia','Tacca integrifolia',32),(38,'Saintpaulia Ionantha','Saintpaulia ionantha',34),(39,'Gaillardia','Gaillardia aestivalis',35),
(40,'Amaryllis','Hippeastrum (group)',36),(44,'Araucaria Heterophylla','Araucaria heterophylla',37),(45,'Begonia','Begonia "Art Hodes"',38),
(46,'Medinilla Magnifica','Medinilla magnifica',39),(50,'Epipremnum Aureum','Epipremnum aureum',1);
GO

INSERT INTO s_delta.plant(plant_id,common_name,origin_id) VALUES 
(1,'Venus flytrap',38),(2,'Corpse flower',2),(3,'Rafflesia arnoldii',1),(4,'Black bat flower',3),(12,'Brugmansia X Candida',9),(13,'Canna "Striata"',10),
(15,'Cuphea "David Verity"',12),(16,'Euphorbia Cotinifolia',13),(18,'Manihot Esculenta "Variegata"',15),(25,'Palm Trees',22),
(37,'Psychopsis Papilio',33),(47,'Calliandra Haematocephala',40),(48,'Zamioculcas Zamiifolia',41),
(49,'Crassula Ovata',42);
GO