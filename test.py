import os
from arcgis.gis import GIS, ContentManager
from arcgis.features import FeatureLayer, FeatureSet

import geopandas as gpd
from arcgis.mapping import WebMap

# from arcgis.apps.survey123 import SurveyManager
# from layer import Layer
# import geopandas as gpd

# from etl.extract import extract
from dotenv import load_dotenv

load_dotenv()


# from layer import Layer
from arcgis.features import FeatureLayerCollection
import json

username = os.getenv("ARCGIS_USERNAME")
password = os.getenv("ARCGIS_PASSWORD")
# storage_folder = os.getenv("ARCGIS_STORAGE_FOLDER")

gis = GIS(username=username, password=password)


# layer_title = "non_overlap_reservation_layer"
# non_overlap_layer = Layer(gis, "non_overlap_reservation_layer", storage_folder, "green")
# # print(non_overlap_layer.layer_item)

# fe_collection = FeatureLayerCollection.fromitem(non_overlap_layer.layer_item)
# # print(fe)
# geoj = {
#   "type": "FeatureCollection",
#   "features": [
#     {
#       "type": "Feature",
#       "properties": {
#         "Que paso con coso": 1234
#       },
#       "geometry": {
#         "coordinates": [
#           [
#             [
#               -66.35626696420208,
#               18.45043547999245
#             ],
#             [
#               -66.40346118917103,
#               18.407580814757893
#             ],
#             [
#               -66.28543432077606,
#               18.407531766168034
#             ],
#             [
#               -66.35626696420208,
#               18.45043547999245
#             ]
#           ]
#         ],
#         "type": "Polygon"
#       }
#     }
#   ]
# }

# with open("./test.geojson", 'w') as f:
#     f.write(json.dumps(geoj))

# fe_collection.manager.overwrite("./test.geojson")


# report_gdf = gpd.read_file("./survey_data/a0abe0ed1451e43129451304660882531.zip")
# report_gdf[]
# print(report_gdf['_qu_ves_ti'].apply(lambda row: row[0:5]))
# print(fe.features
layer_title = "Observaciones"
WEBMAP_TITLE = "Mapa de Costas 2024"
# l = gis.content.search(query=f"title:{layer_title}")

# print(l[0])
webmaps = gis.content.search(query=f"title:{WEBMAP_TITLE}", item_type="Web Map")
# fe = FeatureLayer.fromitem(l[0])
map_item = webmaps[0]
# print(map_item.)
wm = WebMap(map_item)
print(wm.layers[0]["layerDefinition"]["drawingInfo"]["renderer"])

# print(wm.basemap)
# darkGray = gis.content.search('title:light',
# outside_org=True, item_type='web map')[0]
# print(darkGray)
# gis.content.search(query=f"title:", item_type="")
# print(fe.renderer)
# q = fe.query(where="", out_fields=["ObjectId"])
# print(fe.query(where="1=1", out_fields=["id"]))
# object_id = q.features[0].attributes["ObjectId"]

# fe.edit_features(deletes=["905"])

# for f in fe.query(where="id=1", outfields=["ObjectId"]).fields:
# print(f['name'])
# print(f.query(where="==1"))
# print(fe.properties.fields)
# for f in fe.properties.fields:
# print(f['name'])row

# Input:
#   new_map_state en geojson
#

# f = gis.content.search(layer_title)
# print(f)

# report_layer = Layer(gis, "report_layer")

# storage_folder = os.getenv("ARCGIS_STORAGE_FOLDER")

# print("downloading survey data")
# survey_id = os.getenv("SURVEY_TITLE")
# sm = SurveyManager(gis)
# cm = ContentManager(gis)
# report_gdf = extract(survey_id, sm, cm)
# print("Reports ", len(report_gdf))
# # report_gdf = gpd.read_file("./survey_data/ab9f6ca39ac094138944bc94f6b4572c8.zip")

# import pandas as pd

# data1 = {'A': [1, 2, 3, 4], 'B': ['a', 'b', 'c', 'd']}
# data2 = {'A': [2, 3], 'B': ['b', 'c']}

# df_1 = pd.DataFrame(data1)
# df_2 = pd.DataFrame(data2)

# print(df_1)
# # print(df_2)
# # Apply the solution
# result_df = df_1.iloc[1: 4]

# print(result_df)
