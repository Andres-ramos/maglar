
import os 
import time 
from dotenv import load_dotenv
import geopandas as gpd

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
    survey_title = os.getenv("SURVEY_TITLE")
    sm = SurveyManager(gis)
    cm = ContentManager(gis)
    gdf = extract(survey_title, sm, cm)
    # gdf = gpd.read_file("./survey_data/a7f0797af795c420d91e7747c3d228d89.zip")


    print("preprocessing data")
    filtered_gdf = filter_data(gdf)
    # geojson = filtered_gdf.iloc[0:10].to_json()
    # geojson = filtered_gdf.iloc[0:50].to_json()

    print("querying pitirre")
    #TODO: Query against pitirre
    # geojs_dict = {}
    # for i in range(len(filtered_gdf.index)):  
    #     global_id = filtered_gdf.iloc[i]["globalid"]
    #     r = filtered_gdf["geometry"].iloc[i]
    #     geojs_dict[global_id]= query_pitirre(r)

    print("post processing data")
    #TODO: Merge with pitirre
    #TODO: Clean gdf or geojson columns por presentation
    geojson = filtered_gdf.to_json()
    
    print("fetching arcgis state")
    layer_title_name = "layer-geojson-test"
    layer_file_name = "./geojson_data/layer.geojson"
    webmap_title_name = 'Mapa de Costas 2024 WebMap Test'
    storage_folder = os.getenv("ARCGIS_STORAGE_FOLDER")
    
    #TODO: Fix layer update and create logic
    layers = gis.content.search(layer_title_name)
    webmaps = gis.content.search(webmap_title_name)
    protected_area = gis.content.search("g11_conserv_areas_naturales_protegidas_terrestres_2019")[0]

    #If no layers and webmap have been created
    if len(layers) == 0:
        #TODO: Generate more layers 
        #varia por 
        # layer_file_name
        # layer_title_name
        # geojson 
        print("creating layer")
        layer_item = create_layer(
            gis,
            layer_file_name,
            geojson,
            layer_title_name,
            storage_folder
        )
        layer_list = [layer_item]
        print("creating Webmap")
        create_map(
            webmap_title_name,
            layer_list,
            storage_folder
        )

    #If layer and webmaps have already been created 
    else :
        print("updating Layer")
        update_layer(layers, geojson)


    print(f"{time.time()-start} segs")

main()
