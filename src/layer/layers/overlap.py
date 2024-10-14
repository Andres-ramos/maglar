from typing import Any
from typing import Dict

import geopandas as gpd

from ..layer import Layer


# TODO: Clean up
class OverlapLayer(Layer):
    def __init__(self, gis, layer_title, arcgis_storage_folder):
        super().__init__(gis, layer_title, arcgis_storage_folder)

    def generate_layer(self, gdf: gpd.GeoDataFrame) -> Dict[str, Any]:
        RESERVAS_TERRESTRES_FOLDER = "./static/reservas"
        # TODO: Figure out where to put buffer size
        buff_size = 15
        d = gdf["geometry"].to_crs(32620).apply(lambda point: point.buffer(buff_size))
        circle_gdf = gpd.GeoDataFrame({"geometry": d})
        circle_gdf["geometry"] = circle_gdf["geometry"].to_crs(epsg=6566)
        reserve_gdf = gpd.read_file(RESERVAS_TERRESTRES_FOLDER)
        intersecting_gdf = gpd.sjoin(
            reserve_gdf, circle_gdf, how="inner", op="intersects"
        )
        return intersecting_gdf.to_json()

    def generate_style(self):
        return {
            "renderer": {
                "type": "simple",
                "symbol": {
                    "type": "esriSFS",
                    "color": [179, 0, 3, 153],
                    "outline": {
                        "type": "esriSLS",
                        "color": [0, 0, 0, 255],
                        "width": 1.5,
                        "style": "esriSLSSolid",
                    },
                    "style": "esriSFSSolid",
                },
            }
        }
