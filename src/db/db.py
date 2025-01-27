import os
import sqlite3

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
