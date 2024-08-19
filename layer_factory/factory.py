import geopandas as gpd

#TODO: Figure out how to optimize non overlap layer 
#TODO: Figure out where to put the buffer_size 
class LayerFactory:
    def generate_layer(self, layer_name, gdf):
        if layer_name == "report":
            # TODO: Remove columns
            # TODO: Clean column names
            gdf = gdf.drop(columns=['globalid', 'CreationDa', 'Creator', 'EditDate', 'Editor',
                'si_es_una_', 'venta_cont', 'a_ade_come', 'nombre', 'correo_ele',
                'telefono', 'esta_const', 'este_terre', 'si_de_casu', 'pueblo'
                ])
            return gdf.to_json()
        
        elif layer_name == "overlap":
            #TODO: Figure out where to put buffer size 
            buff_size = 15
            d = gdf["geometry"].to_crs(32620).apply(lambda point: point.buffer(buff_size))
            circle_gdf = gpd.GeoDataFrame({"geometry": d})
            circle_gdf["geometry"] = circle_gdf["geometry"].to_crs(epsg=6566)
            reserve_gdf = gpd.read_file("./reservas_terrestres")
            intersecting_gdf = gpd.sjoin(reserve_gdf, circle_gdf, how='inner', op='intersects')
            return intersecting_gdf.to_json()

        elif layer_name == "non_overlap":

            buff_size = 15
            d = gdf["geometry"].to_crs(32620).apply(lambda point: point.buffer(buff_size))
            circle_gdf = gpd.GeoDataFrame({"geometry": d})
            circle_gdf["geometry"] = circle_gdf["geometry"].to_crs(epsg=6566)
            reserve_gdf = gpd.read_file("./reservas_terrestres")
            intersecting_gdf = gpd.sjoin(reserve_gdf, circle_gdf, how='inner', op='intersects')
            non_intersecting_gdf = reserve_gdf[~reserve_gdf.index.isin(intersecting_gdf.index)]
            return non_intersecting_gdf.to_json()
