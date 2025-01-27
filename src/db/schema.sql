CREATE TABLE IF NOT EXISTS Observation (
  id INTEGER PRIMARY KEY,
  globalid TEXT UNIQUE,
  point POINT NOT NULL
);


CREATE TABLE IF NOT EXISTS Parcel (
  id INTEGER PRIMARY KEY,
  pitirreid TEXT UNIQUE,
  geometry GEOMETRY NOT NULL,
  cadastre_number TEXT,
  old_pid TEXT,
  secondary_cadastre_number TEXT,
  owner_name TEXT,
  physical_address TEXT,
  municipality TEXT,
  sold_amount REAL,
  sold_timestamp TEXT,
  seller_name TEXT,
  buyer_name TEXT,
  capacity REAL,
  land_value REAL,
  structure_value REAL,
  machinery_value REAL,
  total_value REAL
);

CREATE TABLE IF NOT EXISTS PUT (
  id INTEGER PRIMARY KEY,
  pitirreid TEXT UNIQUE,
  geometry GEOMETRY NOT NULL
);
