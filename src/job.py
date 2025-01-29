# import json
import os
import time

# import geopandas as gpd
import shapely
from arcgis.apps.survey123 import SurveyManager
from arcgis.gis import GIS
from arcgis.gis import ContentManager
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from shapely.geometry import shape

# from .constants import PUT_LAYER_NAME
# from .constants import REPORT_LAYER_NAME
# from .constants import CLUSTER_LAYER_NAME
# from .constants import FAST_TRACK_LAYER_NAME
# from .constants import NONOVERLAP_LAYER_NAME
# from .constants import OVERLAP_LAYER_NAME
from .constants import ARCGIS_STORAGE_FOLDER
from .constants import PARCEL_LAYER_NAME
from .constants import WEBMAP_TITLE
from .db import initialize
from .etl.extract import extract
from .etl.map import create_map
from .etl.map import create_webmap_properties
from .etl.transform import filter_data
from .layer import LayerFactory
from .logger import logger
from .pytirre import fetch_with_radius
from .utils import find_webmap

load_dotenv()


def job() -> None:
    start = time.time()

    logger.info("Initialiazing database")
    db = initialize()

    logger.info("Logging into arcgis")
    arcgis_username = os.getenv("ARCGIS_USERNAME")
    arcgis_password = os.getenv("ARCGIS_PASSWORD")
    gis = GIS(username=arcgis_username, password=arcgis_password)

    logger.info("Downloading survey data")
    survey_id = os.getenv("SURVEY_TITLE")
    sm = SurveyManager(gis)
    cm = ContentManager(gis)
    report_gdf = extract(survey_id, sm, cm)

    logger.info("Fetching existing records")
    fetch_query = """
                    SELECT globalid FROM Observation;
                """
    result = db.cursor().execute(fetch_query)
    globalIdList = result.fetchall()
    globalIdList = [entry[0] for entry in globalIdList]

    logger.info("Filtering new records")
    report_gdf = report_gdf[~report_gdf["globalid"].isin(globalIdList)]
    logger.info("Inserting new records into database")
    for point, globalid in zip(report_gdf["geometry"], report_gdf["globalid"]):
        point_in_wkt = shapely.to_wkt(point)
        insert_query = """
            INSERT INTO Observation (point, globalid) VALUES (?,?);
        """
        data_to_insert = (point_in_wkt, globalid)
        logger.info("Inserting Observation record")
        db.cursor().execute(insert_query, data_to_insert)
        db.commit()

    logger.info("Preprocessing data")
    report_gdf = report_gdf.to_crs(4326)
    # Filters data spatially
    # TODO: Consider removing columns at this point
    filtered_report_gdf = filter_data(report_gdf)
    filtered_report_gdf = filtered_report_gdf.drop(columns=["index_right"])
    # TODO: Excel de esto
    new_reports_gdf = filtered_report_gdf

    logger.info("Querrying Pitirre")
    pitirre_username = os.getenv("PITIRRE_USERNAME")
    pitirre_password = os.getenv("PITIRRE_PASSWORD")
    pitirre_base_url = os.getenv("PITIRRE_BASE_URL")
    pitirre_parcel_url = os.getenv("PITIRRE_PARCEL_URL")
    # pitirre_put_url = os.getenv("PITIRRE_PUT_URL")

    auth = HTTPBasicAuth(pitirre_username, pitirre_password)

    RADIUS = 15
    points = new_reports_gdf["geometry"]

    logger.info("Fetching from Parcel API")
    for point in points:
        parcel_payload = fetch_with_radius(
            point, pitirre_base_url + pitirre_parcel_url, RADIUS, auth
        )
        for feature in parcel_payload["features"]:
            geometry_in_wkt = shape(feature["geometry"]).wkt
            pitirre_id = feature["id"]
            cadastre_number = feature["properties"]["cadastre_number"]
            old_pid = feature["properties"]["old_pid"]
            secondary_cadastre_number = feature["properties"][
                "secondary_cadastre_number"
            ]
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
                );
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
            db.cursor().execute(insert_query, data_to_insert)
            db.commit()

    # logger.info("Fetching from PUT API")
    # put_list = fetch_with_radius(
    #     points, pitirre_base_url + pitirre_put_url, RADIUS, auth
    # )
    # put_geojson = {"type": "FeatureCollection", "features": put_list}
    # with open("./static/geojson_data/PUT.geojson", "w") as f:
    #     f.write(json.dumps(put_geojson))

    logger.info("Instantiating layers in factory")
    factory = LayerFactory(gis, db)
    layer_list = [
        # factory.generate_layer(OVERLAP_LAYER_NAME),
        # factory.generate_layer(NONOVERLAP_LAYER_NAME),
        # factory.generate_layer(REPORT_LAYER_NAME),
        # factory.generate_layer(CLUSTER_LAYER_NAME),
        # factory.generate_layer(FAST_TRACK_LAYER_NAME),
        factory.generate_layer(PARCEL_LAYER_NAME),
        # factory.generate_layer(PUT_LAYER_NAME),
    ]

    logger.info("Querring existing maps")
    p_webmaps = gis.content.search(query=f"title:{WEBMAP_TITLE}", item_type="Web Map")
    # Finds the correct webmap item and creates webmap object
    wm = find_webmap(p_webmaps, WEBMAP_TITLE)
    if wm is None:
        logger.info("Creating webmap")
        wm = create_map(WEBMAP_TITLE, ARCGIS_STORAGE_FOLDER)

    logger.info("Creating or updating layers")
    # Creates or updates layers
    for layer in layer_list:
        # Creates or updates layer
        logger.info(f"Generating layer : {layer.layer_title}")
        layer_geojson = layer.generate_layer_geojson(new_reports_gdf)
        logger.info(f"Uploading layer : {layer.layer_title}")
        output = layer.update_or_create(layer_geojson)
        # If layer is created, add to webmap
        if output == "create":
            style = layer.generate_style()
            wm.add_layer(layer.layer_item, style)
            wm.update(item_properties=create_webmap_properties(WEBMAP_TITLE))

    logger.info(f"Time to run script {time.time()-start} segs")
