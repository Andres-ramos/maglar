
import os 
import time 
from dotenv import load_dotenv
import geopandas as gpd
import json

from arcgis.gis import GIS, ContentManager
from arcgis.apps.survey123 import SurveyManager
from arcgis.mapping import WebMap
from arcgis.features import FeatureLayerCollection
# from arcgis.mapping import 

from etl.extract import extract  
from etl.transform import filter_data

from typing import List, Any
from layer import LayerFactory

from arcgis2geojson import arcgis2geojson

from utils import find_webmap

from etl.map import create_layer, create_map, update_layer, create_style, create_webmap_properties

from constants import (
    ARCGIS_STORAGE_FOLDER,
    WEBMAP_TITLE,
    REPORT_LAYER_NAME,
    OVERLAP_LAYER_NAME,
    NONOVERLAP_LAYER_NAME,
    CLUSTER_LAYER_NAME,
    FAST_TRACK_LAYER_NAME
)

load_dotenv()

#TODO: Add logger

def main() -> None:
    start = time.time()
    # storage_folder = os.getenv("ARCGIS_STORAGE_FOLDER")
    username = os.getenv("ARCGIS_USERNAME")
    password = os.getenv("ARCGIS_PASSWORD")

    print("logging into arcgis")
    gis = GIS(username=username, password=password)

    print("downloading survey data")
    survey_id = os.getenv("SURVEY_TITLE")
    sm = SurveyManager(gis)
    cm = ContentManager(gis)
    report_gdf = extract(survey_id, sm, cm)

    print("preprocessing data")
    report_gdf = report_gdf.to_crs(6566)
    #Filters data spatially
    #TODO: Consider removing columns at this point
    filtered_report_gdf = filter_data(report_gdf)
    filtered_report_gdf = filtered_report_gdf.drop(columns=['index_right'])
    new_reports_gdf = filtered_report_gdf

    # #TODO: Query againstsurvey_data survey_datapitirre
    # # geojs_dict = {}
    # # for i in range(len(filtered_gdf.index)):  
    # #     global_id = filtered_gdf.iloc[i]["globalid"]
    # #     r = filtered_gdf["geometry"].iloc[i]
    # #     geojs_dict[global_id]= query_pitirre(r)


    #Generate layers from reports 
    factory = LayerFactory(gis)

    #TODO: ADD fast tract layer and cluster layer
    layer_list = [
        factory.generate_layer(OVERLAP_LAYER_NAME),
        factory.generate_layer(NONOVERLAP_LAYER_NAME),
        factory.generate_layer(REPORT_LAYER_NAME),
        factory.generate_layer(CLUSTER_LAYER_NAME),
        factory.generate_layer(FAST_TRACK_LAYER_NAME)
    ]

    p_webmaps = gis.content.search(query=f"title:{WEBMAP_TITLE}", item_type="Web Map")

    #Finds the correct webmap item and creates webmap object
    wm = find_webmap(p_webmaps, WEBMAP_TITLE)
    if wm == None:
        wm = create_map(
            WEBMAP_TITLE,
            ARCGIS_STORAGE_FOLDER
        )   

    #Creates or updates layers 
    for layer in layer_list:
        #Creates or updates layer
        layer_geojson = layer.generate_layer(new_reports_gdf)
        # print(layer_geojson)
        output = layer.update_or_create(layer_geojson)
        #If layer is created, add to webmap
        if output == "create":
            style = layer.generate_style()
            wm.add_layer(layer.layer_item, style)
            wm.update(
                item_properties=create_webmap_properties(WEBMAP_TITLE)
            )

    print(f"{time.time()-start} segs")


main()
