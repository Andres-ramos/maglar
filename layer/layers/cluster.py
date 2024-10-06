import geopandas as gpd
from ..layer import Layer

#TODO: Implement!!
class ClusterLayer(Layer):
    def __init__(self, gis, layer_title, arcgis_storage_folder, color):
        super().__init__(gis, layer_title, arcgis_storage_folder, color)

    def generate_layer(self, gdf):
       pass 