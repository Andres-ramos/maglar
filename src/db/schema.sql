CREATE TABLE IF NOT EXISTS Observation (
  id INTEGER PRIMARY KEY,
  objectid TEXT UNIQUE NOT NULL, --ObjectID
  globalid TEXT UNIQUE NOT NULL, --GlobalID
  creation_date TEXT NOT NULL, --CreationDate
  creator TEXT NOT NULL, --Creator
  edit_date TEXT, --EditDate
  editor TEXT, --Editor
  primary_observation STRING NOT NULL, --¿Qué ves? Tipo de observación
  construction_and_sign INTEGER, --Si es una construcción, ¿tiene rótulos (carteles)  de permisos de alguna agencia gubernamental?
  sale_and_construction INTEGER, --Si es una venta ¿hay alguna construcción en ella?
  sale_and_sign INTEGER, --Si es una venta, ¿tiene rótulos (carteles)  de permisos de alguna agencia gubernamental?
  abandoned_prop_in_water INTEGER, --Si es una estructura abandona, ¿está dentro del mar?
  problem_recording_location INTEGER, --¿Tuvo problemas para entrar la localización en el mapa presentado en la pregunta anterior?
  address TEXT, --Si tienes problemas con el localizador de la pregunta anterior, escribe aquí tu ubicación ya sea pegando desde  google maps o escribiendo el nombre de la calle, el barrio, km y otra descripción.
  municipality TEXT NOT NULL, --Pueblo en donde se está haciendo la observación
  comment TEXT, --Añade comentarios, características o mayor descripción.
  observer_name TEXT, --Nombre y Apellidos
  observer_email TEXT, --Correo electrónico
  observer_phone_number TEXT, --Teléfono
  general_comment TEXT, --Comentarios generales
  other_observations_nearby TEXT, --¿Hay alguna otra observación en el mismo lugar?
  other_observation_categories TEXT, --¿Qué otras observaciones viste? Selecciona todas las que apliquen.
  point POINT NOT NULL,
  noisy_point POINT NOT NULL
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
