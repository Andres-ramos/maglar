import os

DATABASE_SCHEMA_URL = f"{os.path.dirname(__file__)}/schema.sql"

GLOBAL_ID = "GlobalID"
OBJECT_ID = "ObjectID"
CREATION_DATE = "CreationDate"
CREATOR = "Creator"
EDIT_DATE = "EditDate"
EDITOR = "Editor"
PRIMARY_OBSERVATION = "¿Qué ves? Tipo de observación"
CONSTRUCTION_AND_SIGN = "Si es una construcción, ¿tiene rótulos (carteles)  de permisos de alguna agencia gubernamental?"  # noqa
SALE_AND_CONSTRUCTION = "Si es una venta ¿hay alguna construcción en ella?"
SALE_AND_SIGN = "Si es una venta, ¿tiene rótulos (carteles)  de permisos de alguna agencia gubernamental? "  # noqa
ABANDONED_PROP_IN_WATER = "Si es una estructura abandona, ¿está dentro del mar?"
PROBLEM_RECORDING_LOCATION = "¿Tuvo problemas para entrar la localización en el mapa presentado en la pregunta anterior?"  # noqa
ADDRESS = "Si tienes problemas con el localizador de la pregunta anterior, escribe aquí tu ubicación ya sea pegando desde  google maps o escribiendo el nombre de la calle, el barrio, km y otra descripción."  # noqa
MUNICIPALITY = "Pueblo en donde se está haciendo la observación"
COMMENT = "Añade comentarios, características o mayor descripción."
OBSERVER_NAME = "Nombre y Apellidos"
OBSERVER_EMAIL = "Correo electrónico"
OBSERVER_PHONE_NUMBER = "Teléfono"
GENERAL_COMMENTS = "Comentarios generales"
OTHER_OBSERVARVATIONS_NEARBY = "¿Hay alguna otra observación en el mismo lugar?"
OTHER_OBSERVATIONS_CATEGORIES = (
    "¿Qué otras observaciones viste? Selecciona todas las que apliquen."
)
