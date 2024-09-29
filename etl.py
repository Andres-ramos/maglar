
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
from etl.map import create_layer, create_map, update_layer, create_style, create_webmap_properties

from typing import List, Any
from layer_factory import LayerFactory

from layer import Layer
from arcgis2geojson import arcgis2geojson


load_dotenv()

def main() -> None:
    start = time.time()
    factory = LayerFactory()
    storage_folder = os.getenv("ARCGIS_STORAGE_FOLDER")
    username = os.getenv("ARCGIS_USERNAME")
    password = os.getenv("ARCGIS_PASSWORD")

    print("logging into arcgis")
    gis = GIS(username=username, password=password)

    report_layer = Layer(gis, "report_layer", storage_folder, None)
    overlap_layer = Layer(gis, "over_reservation_layer", storage_folder, "red")
    non_overlap_layer = Layer(gis, "non_overlap_reservation_layer", storage_folder, "green")

    print("downloading survey data")
    survey_id = os.getenv("SURVEY_TITLE")
    sm = SurveyManager(gis)
    cm = ContentManager(gis)
    report_gdf = extract(survey_id, sm, cm)
    # print("Reports ", len(report_gdf))
    # report_gdf = gpd.read_file("./survey_data/a180c66d204f34a1aa15f9fd3861c9f03.zip")

    # print("preprocessing data")
    report_gdf = report_gdf.to_crs(6566)
    filtered_report_gdf = filter_data(report_gdf)
    filtered_report_gdf = filtered_report_gdf.drop(columns=['index_right'])
    new_reports_gdf = filtered_report_gdf
    #Finds newest reports
    # new_reports_gdf = get_new_reports(report_layer, filtered_report_gdf)
    # #If no reports, return
    # if len(new_reports_gdf) == 0:
    #     return 
    

    # #TODO: Query againstsurvey_data survey_datapitirre
    # # geojs_dict = {}
    # # for i in range(len(filtered_gdf.index)):  
    # #     global_id = filtered_gdf.iloc[i]["globalid"]
    # #     r = filtered_gdf["geometry"].iloc[i]
    # #     geojs_dict[global_id]= query_pitirre(r)

    # if len(new_reports_gdf) > 0:

    #Generate layer from new_reports 
    report_geojson = factory.generate_layer("report", new_reports_gdf)
    overlap_reserve_geojson = factory.generate_layer("overlap", new_reports_gdf)
    non_overlap_reserve_geojson =  factory.generate_layer("non_overlap", new_reports_gdf)

    layer_list = [
        {"layer":report_layer, "geojson": report_geojson},
        {"layer":overlap_layer, "geojson": overlap_reserve_geojson},
        {"layer":non_overlap_layer, "geojson": non_overlap_reserve_geojson}
    ]

    #Creates webmap 
    webmap_title_name = 'Mapa de Costas 2024 WebMap Test'
    p_webmaps = gis.content.search(query=f"title:{webmap_title_name}", item_type="Web Map")

    #Finds the correct webmap item and creates webmap object
    wm = find_webmap(p_webmaps, webmap_title_name)
    if wm == None:
        print("creating Webmap")
        wm = create_map(
            webmap_title_name,
            None,
            storage_folder
        )   

    #Creates or updates layers 
    for layer in layer_list:
        output = layer["layer"].update_or_create(layer["geojson"])
        if output == "create":
            wm.add_layer(layer["layer"].layer_item, layer["layer"].layer_style)
            wm.update(
                item_properties=create_webmap_properties(webmap_title_name)
            )

    print(f"{time.time()-start} segs")


def find_webmap(p_webmaps, webmap_title_name):
    if len(p_webmaps) == 0:
        wm = None
    #Find webmap
    elif len(p_webmaps) == 1 :
        wm = WebMap(p_webmaps[0])
    else :
        wm = None
        for p_webmap in p_webmaps:
            if p_webmap.title == webmap_title_name and p_webmap.type == "Web Map":
                wm = WebMap(p_webmap)
    return wm

def get_new_reports(report_layer, filtered_report_gdf):
    if report_layer.layer_item != None:
        #Find layer
        l = FeatureLayerCollection.fromitem(report_layer.layer_item).layers[0]
        #convert to geodataframe
        old_reports = l.query().sdf

        if len(filtered_report_gdf) > len(old_reports):
            new_reports_gdf = filtered_report_gdf.iloc[len(old_reports): len(filtered_report_gdf)]
        else :
            new_reports_gdf = gpd.GeoDataFrame({"geometry": []})

        return new_reports_gdf

    #If no layers have been created yet 
    # first run of the server
    new_reports_gdf = filtered_report_gdf
    return new_reports_gdf 

main()
