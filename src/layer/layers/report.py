from typing import Any
from typing import Dict

import geopandas as gpd

from ..layer import Layer


# TODO: Cleanup
class ReportLayer(Layer):
    def __init__(self, gis, layer_title, arcgis_storage_folder):
        super().__init__(gis, layer_title, arcgis_storage_folder)

    def generate_layer(self, gdf: gpd.GeoDataFrame) -> Dict[str, Any]:
        gdf = gdf.drop(
            columns=[
                "CreationDa",
                "Creator",
                "EditDate",
                "Editor",
                "tel_fono",
                "nombre_y_a",
                "correo_ele",
                "categoria",
                "si_es_cons",
                "pregunta_s",
                "_se_puede_",
                "si_es_una_",
                "si_es_una1",
                "si_es_un_1",
                "si_es_un_2",
                "_tuvo_prob",
                "si_tienes_",
                "a_ade_come",
                "comentario",
                "field_21_o",
                "_hay_algun",
            ]
        )
        gdf = gdf.rename(
            columns={
                "_qu_ves_ti": "¿Qué ves? Tipo de observación",
                "pueblo_en_": "Pueblo",
                "_hay_otras": "¿Hay otras observaciones aledañas al lugar?",
                "_se_pudo_o": "¿Qué otras observaciones viste?",
            }
        )
        return gdf.to_json()

    def generate_style(self) -> Dict[str, Any]:
        return {
            "renderer": {
                "type": "simple",
                "symbol": {
                    "type": "esriSMS",
                    "color": [247, 92, 3, 217],
                    "angle": 0,
                    "xoffset": 0,
                    "yoffset": 0,
                    "size": 7.5,
                    "style": "esriSMSCircle",
                    "outline": {
                        "type": "esriSLS",
                        "color": [255, 255, 255, 128],
                        "width": 0.998,
                        "style": "esriSLSSolid",
                    },
                },
            }
        }
