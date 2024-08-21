
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

    print("logging into arcgis")
    username = os.getenv("ARCGIS_USERNAME")
    password = os.getenv("ARCGIS_PASSWORD")
    gis = GIS(username=username, password=password)

    report_layer = Layer(gis, "report_layer", storage_folder)
    # overlap_layer = Layer(gis, "over_reservation_layer")
    # non_overlap_layer = Layer(gis, "non_overlap_reservation_layer")

    
    print("downloading survey data")
    # survey_id = os.getenv("SURVEY_TITLE")
    # sm = SurveyManager(gis)
    # cm = ContentManager(gis)
    # report_gdf = extract(survey_id, sm, cm)
    # print("Reports ", len(report_gdf))
    report_gdf = gpd.read_file("./survey_data/a0e713030126f4e12a9744508bc0ec566.zip")

    print("preprocessing data")
    report_gdf = report_gdf.to_crs(6566)
    filtered_report_gdf = filter_data(report_gdf)
    filtered_report_gdf = filtered_report_gdf.drop(columns=['index_right'])
    #TODO: 
    # l = FeatureLayerCollection.fromitem(report_layer.layer_item).layers[0]
    # print(l.crs)
    # old_reports = l.query().sdf
    # print(old_reports.crs)
    # old_reports["geometry"] = old_reports["SHAPE"].apply(lambda argic_geom: argic_geom.as_shapely)
    # old_reports_gdf = gpd.GeoDataFrame(old_reports)
    # print(old_reports_gdf)
    # Extract layer data as geodataframe
    # Compare against filtered_report_gdf 
    # Find new ones
    # Pass that to the generate layer thing

    print("querying pitirre")
    #TODO: Query againstsurvey_data survey_datapitirre
    # geojs_dict = {}
    # for i in range(len(filtered_gdf.index)):  
    #     global_id = filtered_gdf.iloc[i]["globalid"]
    #     r = filtered_gdf["geometry"].iloc[i]
    #     geojs_dict[global_id]= query_pitirre(r)

    print("processing data")
    #TODO: Add code from notebook that creates the dataframes

    # factory = LayerFactory()
    report_geojson = factory.generate_layer("report", filtered_report_gdf)
    # overlap_reserve_geojson = factory.generate_layer("overlap", filtered_report_gdf)
    # non_overlap_reserve_geojson =  factory.generate_layer("non_overlap", filtered_report_gdf)

    layer_list = [
        report_layer,
        # overlap_layer,
        # non_overlap_layer
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
        output = layer.update_or_create(wm, report_geojson)
        if output == "create":
            wm.add_layer(layer.layer_item, layer.layer_style)
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
    return 

main()
