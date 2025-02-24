import os
import random
import sqlite3

import shapely
from shapely.geometry import shape

from ..logger import logger
from .constants import ABANDONED_PROP_IN_WATER
from .constants import ADDRESS
from .constants import COMMENT
from .constants import CONSTRUCTION_AND_SIGN
from .constants import CREATION_DATE
from .constants import CREATOR
from .constants import DATABASE_SCHEMA_URL
from .constants import EDIT_DATE
from .constants import EDITOR
from .constants import GENERAL_COMMENTS
from .constants import GLOBAL_ID
from .constants import MUNICIPALITY
from .constants import OBJECT_ID
from .constants import OBSERVER_EMAIL
from .constants import OBSERVER_NAME
from .constants import OBSERVER_PHONE_NUMBER
from .constants import OTHER_OBSERVARVATIONS_NEARBY
from .constants import OTHER_OBSERVATIONS_CATEGORIES
from .constants import PRIMARY_OBSERVATION
from .constants import PROBLEM_RECORDING_LOCATION
from .constants import SALE_AND_CONSTRUCTION
from .constants import SALE_AND_SIGN
from .exceptions import DBInsertObservationException


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
        # TODO: Insert reservas naturales y zmt layer
    # gets db connection object
    db = get_db(db_name)

    return db


def insert_observations(db, filtered_records):
    for _, payload in filtered_records.iterrows():
        try:
            insert_observation(db, payload)
        except Exception:
            logger.warning("Failed to insert observation")
            pass


def insert_observation(db, payload):
    global_id = payload[GLOBAL_ID]
    object_id = payload[OBJECT_ID]
    creation_date = payload[CREATION_DATE]
    creator = payload[CREATOR]
    edit_date = payload[EDIT_DATE]
    editor = payload[EDITOR]
    primary_observation = payload[PRIMARY_OBSERVATION]
    construction_and_sign = payload[CONSTRUCTION_AND_SIGN]
    sale_and_construction = payload[SALE_AND_CONSTRUCTION]
    sale_and_sign = payload[SALE_AND_SIGN]
    abandoned_prop_in_water = payload[ABANDONED_PROP_IN_WATER]
    problem_recording_location = payload[PROBLEM_RECORDING_LOCATION]
    address = payload[ADDRESS]
    municipality = payload[MUNICIPALITY]
    comment = payload[COMMENT]
    observer_name = payload[OBSERVER_NAME]
    observer_email = payload[OBSERVER_EMAIL]
    observer_phone_number = payload[OBSERVER_PHONE_NUMBER]
    general_comment = payload[GENERAL_COMMENTS]
    other_observations_nearby = payload[OTHER_OBSERVARVATIONS_NEARBY]
    other_observation_categories = payload[OTHER_OBSERVATIONS_CATEGORIES]

    lat, lng = float(payload["y"]), float(payload["x"])
    point = shapely.Point(lng, lat)
    point_in_wkt = point.wkt

    noisy_point = generate_noisy_point(point)
    noisy_point_in_wkt = noisy_point.wkt

    insert_query = """
        INSERT INTO Observation (
            globalid,
            objectid,
            creation_date,
            creator,
            edit_date,
            editor,
            primary_observation,
            construction_and_sign,
            sale_and_construction,
            sale_and_sign,
            abandoned_prop_in_water,
            problem_recording_location,
            address,
            municipality,
            comment,
            observer_name,
            observer_email,
            observer_phone_number,
            general_comment,
            other_observations_nearby,
            other_observation_categories,
            point,
            noisy_point
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? , ?
        ) ON CONFLICT(globalid) DO NOTHING;
    """
    data_to_insert = (
        global_id,
        object_id,
        creation_date,
        creator,
        edit_date,
        editor,
        primary_observation,
        construction_and_sign,
        sale_and_construction,
        sale_and_sign,
        abandoned_prop_in_water,
        problem_recording_location,
        address,
        municipality,
        comment,
        observer_name,
        observer_email,
        observer_phone_number,
        general_comment,
        other_observations_nearby,
        other_observation_categories,
        point_in_wkt,
        noisy_point_in_wkt,
    )
    logger.info("Inserting Observation record")
    try:
        db.cursor().execute(insert_query, data_to_insert)
        db.commit()
    except Exception as e:
        logger.error(f"Error: Observation failed to insert {e}")
        raise DBInsertObservationException


def generate_noisy_point(point: float, range: float = 0.0001):
    noisy_x = point.x + random.uniform(-range, range)
    noisy_y = point.y + random.uniform(-range, range)
    return shapely.Point(noisy_x, noisy_y)


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
