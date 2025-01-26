from typing import Any
from typing import Dict

import geopandas as gpd

from ..layer import Layer


class ParcelLayer(Layer):
    def __init__(self, gis, layer_title, arcgis_storage_folder):
        super().__init__(gis, layer_title, arcgis_storage_folder)

    def generate_layer_geojson(self, gdf: gpd.GeoDataFrame) -> Dict[str, Any]:
        PARCEL_DATA = "./static/geojson_data/parcels.geojson"
        parcel_gdf = gpd.read_file(PARCEL_DATA)
        return parcel_gdf.to_json()

    def generate_style(self):
        return {}
