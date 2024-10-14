import geopandas as gpd
from ..layer import Layer

#TODO: Clean up
class NonOverlapLayer(Layer):
    def __init__(self, gis, layer_title, arcgis_storage_folder, color):
        super().__init__(gis, layer_title, arcgis_storage_folder, color)

    def generate_layer(self, gdf):
        RESERVAS_TERRESTRES_FOLDER = "./static/reservas"
        buff_size = 15
        d = gdf["geometry"].to_crs(32620).apply(lambda point: point.buffer(buff_size))
        circle_gdf = gpd.GeoDataFrame({"geometry": d})
        circle_gdf["geometry"] = circle_gdf["geometry"].to_crs(epsg=6566)
        reserve_gdf = gpd.read_file(RESERVAS_TERRESTRES_FOLDER)
        intersecting_gdf = gpd.sjoin(reserve_gdf, circle_gdf, how='inner', op='intersects')
        non_intersecting_gdf = reserve_gdf[~reserve_gdf.index.isin(intersecting_gdf.index)]
        # non_intersecting_gdf = non_intersecting_gdf.drop(columns=[ 'loc_desig','terr_mar', 'gis_source', 'notes'])
        # non_intersecting_gdf = non_intersecting_gdf.rename(columns={
        #     "names": "Nombre",
        #     "mgmt": "Manejador",
        #     "ownership": "Dueño",
        #     "year_estab": "Año establecida"
        # })
        return non_intersecting_gdf.to_json()


    def generate_style(self):
        return {
            "renderer": {
            "type": "simple",
            "symbol": {
            "type": "esriSFS",
            "color": [
                0,
                0,
                0,
                0
            ],
            "outline": {
                "type": "esriSLS",
                "color": [
                74,
                124,
                89,
                191
                ],
                "width": 0.75,
                "style": "esriSLSSolid"
            },
            "style": "esriSFSSolid"
            }
        }
    }

        