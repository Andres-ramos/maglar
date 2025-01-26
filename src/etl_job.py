import json
import os
import time

import requests
from arcgis.apps.survey123 import SurveyManager
from arcgis.gis import GIS
from arcgis.gis import ContentManager
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

from .constants import ARCGIS_STORAGE_FOLDER
from .constants import CLUSTER_LAYER_NAME
from .constants import FAST_TRACK_LAYER_NAME
from .constants import NONOVERLAP_LAYER_NAME
from .constants import OVERLAP_LAYER_NAME
from .constants import PARCEL_LAYER_NAME
from .constants import PUT_LAYER_NAME
from .constants import REPORT_LAYER_NAME
from .constants import WEBMAP_TITLE
from .etl.extract import extract
from .etl.map import create_map
from .etl.map import create_webmap_properties
from .etl.transform import filter_data
from .layer import LayerFactory
from .logger import logger
from .utils import find_webmap

load_dotenv()


def etl_job() -> None:
    start = time.time()
    arcgis_username = os.getenv("ARCGIS_USERNAME")
    arcgis_password = os.getenv("ARCGIS_PASSWORD")

    logger.info("Logging into arcgis")
    gis = GIS(username=arcgis_username, password=arcgis_password)

    logger.info("Downloading survey data")
    survey_id = os.getenv("SURVEY_TITLE")
    sm = SurveyManager(gis)
    cm = ContentManager(gis)
    report_gdf = extract(survey_id, sm, cm)

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
    pitirre_put_url = os.getenv("PITIRRE_PUT_URL")

    basic = HTTPBasicAuth(pitirre_username, pitirre_password)

    points = new_reports_gdf["geometry"]
    logger.info("Querrying Parcel API")
    parcel_list = []
    for point in points:
        point_str = f"{point.x},{point.y}"
        distance = 15
        params = {"dist": distance, "point": point_str}
        pitirre_response = requests.get(
            pitirre_base_url + pitirre_parcel_url, auth=basic, params=params
        )
        parcel_result = pitirre_response.json()
        parcel_list += parcel_result["results"]["features"]

    parcel_geojson = {"type": "FeatureCollection", "features": parcel_list}
    with open("./static/geojson_data/parcels.geojson", "w") as f:
        f.write(json.dumps(parcel_geojson))

    logger.info("Querrying PUT API")
    put_list = []
    for point in points:
        point_str = f"{point.x},{point.y}"
        distance = 15
        params = {"dist": distance, "point": point_str}
        pitirre_response = requests.get(
            pitirre_base_url + pitirre_put_url, auth=basic, params=params
        )
        put_result = pitirre_response.json()
        put_list += put_result["results"]["features"]
    put_geojson = {"type": "FeatureCollection", "features": put_list}
    with open("./static/geojson_data/PUT.geojson", "w") as f:
        f.write(json.dumps(put_geojson))

    # Generate layers from reports
    factory = LayerFactory(gis)
    layer_list = [
        factory.generate_layer(OVERLAP_LAYER_NAME),
        factory.generate_layer(NONOVERLAP_LAYER_NAME),
        factory.generate_layer(REPORT_LAYER_NAME),
        factory.generate_layer(CLUSTER_LAYER_NAME),
        factory.generate_layer(FAST_TRACK_LAYER_NAME),
        factory.generate_layer(PARCEL_LAYER_NAME),
        factory.generate_layer(PUT_LAYER_NAME),
    ]

    p_webmaps = gis.content.search(query=f"title:{WEBMAP_TITLE}", item_type="Web Map")

    # Finds the correct webmap item and creates webmap object
    wm = find_webmap(p_webmaps, WEBMAP_TITLE)
    if wm is None:
        logger.info("Creating webmap")
        wm = create_map(WEBMAP_TITLE, ARCGIS_STORAGE_FOLDER)

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
