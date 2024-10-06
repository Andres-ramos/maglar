import geopandas as gpd
from .report import ReportLayer
from .overlap import OverlapLayer
from .non_overlap import NonOverlapLayer

class LayerFactory:
    def __init__(self, gis):
        self.gis = gis

    def generate_layer(self, layer_name, gdf):

        if layer_name == "report":
            layer_title = "report_layer"
            report_layer = ReportLayer(
                self.gis, 
                layer_title,
                "Mapa de Costas-2024",
                None
            )
            return report_layer.generate_layer(gdf)
        
        elif layer_name == "overlap":
            layer_title = "over_reservation_layer"
            overlap_layer = OverlapLayer(
                self.gis, 
                layer_title,
                "Mapa de Costas-2024",
                None
            )
            return overlap_layer.generate_layer(gdf)

        elif layer_name == "non_overlap":
            layer_title = "over_reservation_layer"
            non_overlap_layer = NonOverlapLayer(
                self.gis, 
                layer_title,
                "Mapa de Costas-2024",
                None
            )
            return non_overlap_layer.generate_layer(gdf)

        else :
            raise Exception(f"{layer_name} not yet implemented!")