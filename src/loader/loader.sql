# Purge existing tables

DROP TABLE IF EXISTS People, Places;


# Create new tables

CREATE TABLE People(
    given_name VARCHAR(32),
    family_name VARCHAR(32),
    date_of_birth VARCHAR(32),
    place_of_birth VARCHAR(32)
);

CREATE TABLE Places(
    city VARCHAR(32),
    county VARCHAR(32),
    country VARCHAR(32)
);


# Load data from CSV files into tables

LOAD DATA LOCAL INFILE '/data/people.csv' 
INTO TABLE People 
FIELDS TERMINATED BY ',' 
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE '/data/places.csv' 
INTO TABLE Places 
FIELDS TERMINATED BY ',' 
IGNORE 1 LINES;
