from typing import Any
from typing import Dict

import geopandas as gpd

from ..layer import Layer


class PUTLayer(Layer):
    def __init__(self, gis, layer_title, arcgis_storage_folder):
        super().__init__(gis, layer_title, arcgis_storage_folder)

    def generate_layer_geojson(self, gdf: gpd.GeoDataFrame) -> Dict[str, Any]:
        buff_size = 15
        d = gdf["geometry"].to_crs(32620).apply(lambda point: point.buffer(buff_size))
        circle_gdf = gpd.GeoDataFrame({"geometry": d})
        circle_gdf["geometry"] = circle_gdf["geometry"].to_crs(epsg=4326)

        PUT_DATA = "./static/geojson_data/PUT.geojson"
        put_gdf = gpd.read_file(PUT_DATA)
        intersecting_gdf = gpd.clip(put_gdf, circle_gdf)

        return intersecting_gdf.to_json()

    def generate_style(self):
        return {}
