CREATE TABLE IF NOT EXISTS Observation (
  id INTEGER PRIMARY KEY,
  arcgisid TEXT UNIQUE,
  point POINT NOT NULL,
  creation_date TEXT NOT NULL,
  creator TEXT NOT NULL,
  edit_date TEXT,
  editor TEXT,
  category TEXT NOT NULL,
  municipality TEXT NOT NULL,
  observer_name TEXT,
  observer_email TEXT,
  observer_phone_number TEXT,
  problem_reporting INTEGER

  -- si_es_cons
  -- _qu_ves_ti
  -- pregunta_s
  -- _se_puede_
  -- si_es_una_
  -- si_es_una1
  -- si_es_un_1
  -- si_es_un_2
  -- si_tienes_
  -- a_ade_come
  -- _hay_otras

  -- comentario
  -- _se_pudo_o
  -- field_21_o
  -- _hay_algun
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
