import geopandas as gpd
from .layers import ReportLayer
from .layers import OverlapLayer
from .layers import NonOverlapLayer

from constants import (
    ARCGIS_STORAGE_FOLDER,
    WEBMAP_TITLE,
    REPORT_LAYER_NAME,
    OVERLAP_LAYER_NAME,
    NONOVERLAP_LAYER_NAME
)

class LayerFactory:
    def __init__(self, gis):
        self.gis = gis

    def generate_layer(self, layer_name):

        if layer_name == REPORT_LAYER_NAME:
            layer_title = "Observaciones"
            return ReportLayer(
                self.gis, 
                layer_title,
                "Mapa de Costas-2024",
                None
            )
        
        elif layer_name == OVERLAP_LAYER_NAME:
            layer_title = "Reservas Peligrando"
            return OverlapLayer(
                self.gis, 
                layer_title,
                "Mapa de Costas-2024",
                "red"
            )

        elif layer_name == NONOVERLAP_LAYER_NAME:
            layer_title = "Reservas"
            return NonOverlapLayer(
                self.gis, 
                layer_title,
                "Mapa de Costas-2024",
                "green"
            )

        else :
            raise Exception(f"{layer_name} not yet implemented!")