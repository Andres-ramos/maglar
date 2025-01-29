import json
from typing import Any
from typing import Dict

import geopandas as gpd
import shapely

from ..layer import Layer


class ParcelLayer(Layer):
    def __init__(self, gis, db, layer_title, arcgis_storage_folder):
        super().__init__(gis, db, layer_title, arcgis_storage_folder)

    def generate_layer_geojson(self, gdf: gpd.GeoDataFrame) -> Dict[str, Any]:
        # TODO: Evaluate if this query will need to be rewritten
        # For example: there might be more parcels in the db that we don;t
        # want to show
        # TODO: Add all the necesesary values
        q = "SELECT cadastre_number, owner_name, geometry FROM Parcel"
        results = self.db.cursor().execute(q).fetchall()

        feature_list = []
        for result in results:
            # TODO: Extract necessary values
            cadastre_number = result[0]
            owner_name = result[1]
            geom_wkt = result[2]
            polygon = shapely.from_wkt(geom_wkt)

            feature = {
                "type": "Feature",
                "properties": {
                    # TODO: Add new values
                    "Numero de Catastro": cadastre_number,
                    "Dueno de Propiedad": owner_name,
                },
                "geometry": json.loads(shapely.to_geojson(polygon)),
            }

            feature_list.append(feature)

        return json.dumps({"type": "FeatureCollection", "features": feature_list})

    def generate_style(self):
        return {}
