
import os 
import time 
from dotenv import load_dotenv
import geopandas as gpd
import json

from arcgis.gis import GIS, ContentManager
from arcgis.apps.survey123 import SurveyManager

from etl.extract import extract  
from etl.transform import filter_data
from etl.map import create_layer, create_map, update_layer

load_dotenv()

def main() -> None:
    start = time.time()

    print("logging into arcgis")
    username = os.getenv("ARCGIS_USERNAME")
    password = os.getenv("ARCGIS_PASSWORD")
    gis = GIS(username=username, password=password)
    
    print("downloading survey data")
    survey_id = os.getenv("2023_SURVEY_ID")
    sm = SurveyManager(gis)
    cm = ContentManager(gis)
    # report_gdf = extract(survey_id, sm, cm)
    # report_gdf = gpd.read_file("./survey_data/a6830f69f8748455f817f4cbb753859c6.zip")


    print("preprocessing data")
    # filtered_report_gdf = filter_data(report_gdf)

    print("querying pitirre")
    #TODO: Query againstsurvey_data survey_datapitirre
    # geojs_dict = {}
    # for i in range(len(filtered_gdf.index)):  
    #     global_id = filtered_gdf.iloc[i]["globalid"]
    #     r = filtered_gdf["geometry"].iloc[i]
    #     geojs_dict[global_id]= query_pitirre(r)

    print("processing data")
    #TODO: Add code from notebook that creates the dataframes
    # report_geojson = filtered_report_gdf.iloc[0:10].to_json()
    report_geojson = json.dumps({
        "type": "FeatureCollection",
        "features": [
            {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "coordinates": [
                -67.26601508255995,
                18.35533611409808
                ],
                "type": "Point"
            }
            }
        ]
    })
    # overlap_reserve_geojson = filtered_report_gdf.iloc[100:110].to_json()
    overlap_reserve_geojson = json.dumps({
        "type": "FeatureCollection",
        "features": [
            {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "coordinates": [
                -66.55189752369114,
                17.99030563016582
                ],
                "type": "Point"
            }
            }
        ]
    })
    # non_overlap_reserve_geojson =  filtered_report_gdf.iloc[60:70].to_json()
    non_overlap_reserve_geojson = json.dumps({
        "type": "FeatureCollection",
        "features": [
            {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "coordinates": [
                -65.4133124334345,
                18.133905335347478
                ],
                "type": "Point"
            }
            },
            {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "coordinates": [
                -65.51124017122592,
                18.1228120765213
                ],
                "type": "Point"
            }
            }
        ]
    })

    report_layer_title_name = "report_layer"
    overlap_reserve_title_name = "overlap_reservation_layer"
    non_overlap_reserve_title_name = "non_overlap_reservation_layer"


    report_layer_file_name = "./geojson_data/report_layer.geojson"
    overlap_reserve_file_name = "./geojson_data/overlap_layer.geojson"
    non_overlap_reserve_file_name = "./geojson_data/non_overlap_layer.geojson"
 
    layer_metadata_list = [
        {
        "title": report_layer_title_name,
        "file_name": report_layer_file_name,
        "geojson": report_geojson
        },
        {
        "title": overlap_reserve_title_name,
        "file_name": overlap_reserve_file_name,
        "geojson": overlap_reserve_geojson
        },
        {
        "title": non_overlap_reserve_title_name,
        "file_name": non_overlap_reserve_file_name,
        "geojson": non_overlap_reserve_geojson
        },
    ]

    storage_folder = os.getenv("ARCGIS_STORAGE_FOLDER")

    #Creates or updates layers 
    layer_item_list = []
    for layer in layer_metadata_list:
        layers = gis.content.search(layer["title"])
        #If no layers with title name have been created
        if len(layers) == 0:
            print("creating layer")
            layer_item = create_layer(
                gis,
                layer["file_name"],
                layer["geojson"],
                layer["title"],
                storage_folder
            )
            layer_item_list.append(layer_item)
        #If layer and webmaps have already been created 
        else :
            print("updating Layer")
            layer_item = update_layer(layers, layer["geojson"])
            layer_item_list.append(layer_item)

    #Creates webmap 
    webmap_title_name = 'Mapa de Costas 2024 WebMap Test'
    webmaps = gis.content.search(webmap_title_name)
    if len(webmaps) == 0:
        print("creating Webmap")
        create_map(
            webmap_title_name,
            layer_item_list,
            storage_folder
        )

    print(f"{time.time()-start} segs")

main()
