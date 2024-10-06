import geopandas as gpd
from ..layer import Layer

#TODO: Clean up
class OverlapLayer(Layer):
    def __init__(self, gis, layer_title, arcgis_storage_folder, color):
        super().__init__(gis, layer_title, arcgis_storage_folder, color)


    def generate_layer(self, gdf):
        RESERVAS_TERRESTRES_FOLDER = "./static/reservas"
        #TODO: Figure out where to put buffer size 
        buff_size = 15
        d = gdf["geometry"].to_crs(32620).apply(lambda point: point.buffer(buff_size))
        circle_gdf = gpd.GeoDataFrame({"geometry": d})
        circle_gdf["geometry"] = circle_gdf["geometry"].to_crs(epsg=6566)
        reserve_gdf = gpd.read_file(RESERVAS_TERRESTRES_FOLDER)
        intersecting_gdf = gpd.sjoin(reserve_gdf, circle_gdf, how='inner', op='intersects')
        # intersecting_gdf = intersecting_gdf.drop(columns=[ 'loc_desig','terr_mar', 'gis_source', 'notes', 
        # 'index_right'])
        # intersecting_gdf = intersecting_gdf.rename(columns={
        #     "names": "Nombre",
        #     "mgmt": "Manejador",
        #     "ownership": "Dueño",
        #     "year_estab": "Año establecida"
        # })
        return intersecting_gdf.to_json()
