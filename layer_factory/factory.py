import geopandas as gpd
from .report import generate_report_layer 
from .overlap import generate_overlap_layer
from .non_overlap import generate_non_overlap_layer

class LayerFactory:
    def __init__(self, gis):
        self.gis = gis

    def generate_layer(self, layer_name, gdf):

        if layer_name == "report":
            return generate_report_layer(gdf)
        
        elif layer_name == "overlap":
            return generate_overlap_layer(gdf)

        elif layer_name == "non_overlap":
            return generate_non_overlap_layer(gdf)

        else :
            raise Exception(f"{layer_name} not yet implemented!")