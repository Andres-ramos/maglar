import geopandas as gpd
from .layers import ReportLayer
from .layers import OverlapLayer
from .layers import NonOverlapLayer

class LayerFactory:
    def __init__(self, gis):
        self.gis = gis

    def generate_layer(self, layer_name):

        if layer_name == "report":
            layer_title = "report_layer"
            return ReportLayer(
                self.gis, 
                layer_title,
                "Mapa de Costas-2024",
                None
            )
            # return report_layer.generate_layer(gdf)
        
        elif layer_name == "overlap":
            layer_title = "over_reservation_layer"
            return OverlapLayer(
                self.gis, 
                layer_title,
                "Mapa de Costas-2024",
                "red"
            )
            # return overlap_layer.generate_layer(gdf)

        elif layer_name == "non_overlap":
            layer_title = "non_overlap_reservation_layer"
            return NonOverlapLayer(
                self.gis, 
                layer_title,
                "Mapa de Costas-2024",
                "green"
            )
            # return non_overlap_layer.generate_layer(gdf)

        else :
            raise Exception(f"{layer_name} not yet implemented!")