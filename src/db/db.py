import os
import sqlite3

from shapely.geometry import shape

from ..logger import logger
from .constants import DATABASE_SCHEMA_URL


def get_db(db_name):
    db = sqlite3.connect(f"{db_name}.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)

    db.enable_load_extension(True)
    db.load_extension("mod_spatialite")
    return db


def init_db(db_name):
    db = get_db(db_name)
    with open(DATABASE_SCHEMA_URL) as fp:
        db.executescript(fp.read())


def initialize():
    db_name = "db"
    if not os.path.isfile(db_name):
        db = init_db(db_name)
    # gets db connection object
    db = get_db(db_name)

    return db


def insert_observations(db, filtered_records):
    for _, payload in filtered_records.iterrows():
        arcgis_id = payload["globalid"]
        point_in_wkt = shape(payload["geometry"]).wkt
        creation_date = payload["CreationDa"]
        creator = payload["Creator"]
        edit_date = payload["EditDate"]
        editor = payload["Editor"]
        category = payload["_qu_ves_ti"]
        municipality = payload["pueblo_en_"]
        observer_name = payload["nombre_y_a"]
        observer_email = payload["correo_ele"]
        observer_phone_number = payload["tel_fono"]
        problem_reporting = payload["_tuvo_prob"]

        insert_query = """
            INSERT INTO Observation (
                point,
                arcgisid,
                creation_date,
                creator,
                edit_date,
                editor,
                category,
                municipality,
                observer_name,
                observer_email,
                observer_phone_number,
                problem_reporting
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            ) ON CONFLICT(arcgisid) DO NOTHING;
        """
        data_to_insert = (
            point_in_wkt,
            arcgis_id,
            creation_date,
            creator,
            edit_date,
            editor,
            category,
            municipality,
            observer_name,
            observer_email,
            observer_phone_number,
            problem_reporting,
        )
        logger.info("Inserting Observation record")
        try:
            db.cursor().execute(insert_query, data_to_insert)
            db.commit()
        except Exception as e:
            logger.error(f"Error: Observation failed to insert {e}")

    return


def insert_parcel(db, feature):
    geometry_in_wkt = shape(feature["geometry"]).wkt
    pitirre_id = feature["id"]
    cadastre_number = feature["properties"]["cadastre_number"]
    old_pid = feature["properties"]["old_pid"]
    secondary_cadastre_number = feature["properties"]["secondary_cadastre_number"]
    owner_name = feature["properties"]["owner_name"]
    physical_address = feature["properties"]["physical_address"]
    municipality = feature["properties"]["municipality"]
    sold_amount = feature["properties"]["sold_amount"]
    sold_timestamp = feature["properties"]["sold_timestamp"]
    seller_name = feature["properties"]["seller_name"]
    buyer_name = feature["properties"]["buyer_name"]
    capacity = feature["properties"]["capacity"]
    land_value = feature["properties"]["land_value"]
    structure_value = feature["properties"]["structure_value"]
    machinery_value = feature["properties"]["machinery_value"]
    total_value = feature["properties"]["total_value"]

    insert_query = """
        INSERT INTO Parcel (
            geometry,
            pitirreid,
            cadastre_number,
            old_pid,
            secondary_cadastre_number,
            owner_name,
            physical_address,
            municipality,
            sold_amount,
            sold_timestamp,
            seller_name,
            buyer_name,
            capacity,
            land_value,
            structure_value,
            machinery_value,
            total_value
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        ) ON CONFLICT(pitirreid) DO NOTHING;
    """
    data_to_insert = (
        geometry_in_wkt,
        pitirre_id,
        cadastre_number,
        old_pid,
        secondary_cadastre_number,
        owner_name,
        physical_address,
        municipality,
        sold_amount,
        sold_timestamp,
        seller_name,
        buyer_name,
        capacity,
        land_value,
        structure_value,
        machinery_value,
        total_value,
    )
    logger.info("Inserting Parcel record")
    try:
        db.cursor().execute(insert_query, data_to_insert)
        db.commit()
    except Exception as e:
        logger.error(f"Error: Parcel failed to insert {e}")


def insert_put_parcel():
    return


# 'ObjectID',
# 'GlobalID',
# 'CreationDate',
# 'Creator',
# 'EditDate',
# 'Editor',
# 'Categoria',
# 'Si es construccion tiene rotulos?', 'si_es_cons
# '¿Qué ves? Tipo de observación', '_qu_ves_ti'
# 'Otro - ¿Qué ves? Tipo de observación', 'pregunta_s'
# '¿Se puede observar más de una situación de
# la observada anteriormente? Favor de indicarlo.', '_se_puede_'
# 'Si es una venta ¿hay alguna construcción en
# ella?', si_es_una_'
# 'Si es una venta, ¿tiene rótulos (carteles)
# de permisos de alguna agencia gubernamental? ', si_es_una1
# 'Si es una construcción, ¿tiene rótulos (carteles)
# de permisos de alguna agencia gubernamental?', 'si_es_un_1
# 'Si es una estructura abandona, ¿está dentro del
# mar?', 'si_es_un_2'
# '¿Tuvo problemas para entrar la localización en el mapa
#  presentado en la pregunta anterior?', '_tuvo_prob'
# 'Si tienes problemas con el localizador de la
# pregunta anterior, escribe aquí tu ubicación ya sea
# pegando desde  google maps o escribiendo el nombre
# de la calle, el barrio, km y otra descripción.', 'si_tienes_'
# 'Pueblo en donde se está haciendo la observación', 'pueblo_en_'
# 'Añade comentarios, características o mayor descripción.', 'a_ade_come'
# '¿Hay otras observaciones aledañas al lugar?
#  Favor de escribirlas. ', _hay_otras'
# 'Nombre y Apellidos', 'Correo electrónico', 'Teléfono',
# 'Comentarios generales',
# '¿Qué otras observaciones viste? Selecciona todas las
# que apliquen.',  '_se_pudo_o'
# 'Otro - ¿Qué otras observaciones viste? Selecciona todas
# las que apliquen.', 'field_21_o'
# '¿Hay alguna otra observación en el mismo lugar?',  '_hay_algun'
