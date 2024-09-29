import geopandas as gpd

class LayerFactory:
    def __init__(self):
        self.RESERVAS_TERRESTRES_FOLDER = "./reservas_marinas"

    def generate_layer(self, layer_name, gdf):
        if layer_name == "report":
            # TODO: Clean column names
            gdf = gdf.drop(columns=['CreationDa', 'Creator', 'EditDate', 'Editor',
                'tel_fono', 'nombre_y_a', 'correo_ele', 'categoria', 'si_es_cons',
                'pregunta_s', '_se_puede_', 'si_es_una_', 'si_es_una1', 'si_es_un_1', 
                'si_es_un_2', '_tuvo_prob', 'si_tienes_', 'a_ade_come', 'comentario', 
                'field_21_o', '_hay_algun'])
            gdf = gdf.rename(columns={
                "_qu_ves_ti": "¿Qué ves? Tipo de observación", 
                "pueblo_en_": "Pueblo",
                "_hay_otras": "¿Hay otras observaciones aledañas al lugar?",
                "_se_pudo_o": "¿Qué otras observaciones viste?"
                })
            # column_map = {
            #     "": "¿Hay otras observaciones aledañas al lugar?",
            #     "": "¿Qué otras observaciones viste?",
            #     "": "¿Hay alguna otra observación en el mismo lugar?",
            #     "": "¿Se puede observar más de una situación de la observada anteriormente?",
            #     "": "Añade comentarios, características o mayor descripción."
            #     "": "Comentarios generales"
            # }
            # gdf['test_col'] = gdf['_qu_ves_ti'].apply(lambda row: row[0:5])

            return gdf.to_json()
        
        elif layer_name == "overlap":
            #TODO: Figure out where to put buffer size 
            buff_size = 15
            d = gdf["geometry"].to_crs(32620).apply(lambda point: point.buffer(buff_size))
            circle_gdf = gpd.GeoDataFrame({"geometry": d})
            circle_gdf["geometry"] = circle_gdf["geometry"].to_crs(epsg=6566)
            reserve_gdf = gpd.read_file(self.RESERVAS_TERRESTRES_FOLDER)
            intersecting_gdf = gpd.sjoin(reserve_gdf, circle_gdf, how='inner', op='intersects')
            print(intersecting_gdf)
            intersecting_gdf = intersecting_gdf.drop(columns=[ 'loc_desig','terr_mar', 'gis_source', 'notes', 
            'index_right'])
            intersecting_gdf = intersecting_gdf.rename(columns={
                "names": "Nombre",
                "mgmt": "Manejador",
                "ownership": "Dueño",
                "year_estab": "Año establecida"
            })
            return intersecting_gdf.to_json()

        elif layer_name == "non_overlap":

            buff_size = 15
            d = gdf["geometry"].to_crs(32620).apply(lambda point: point.buffer(buff_size))
            circle_gdf = gpd.GeoDataFrame({"geometry": d})
            circle_gdf["geometry"] = circle_gdf["geometry"].to_crs(epsg=6566)
            reserve_gdf = gpd.read_file(self.RESERVAS_TERRESTRES_FOLDER)
            intersecting_gdf = gpd.sjoin(reserve_gdf, circle_gdf, how='inner', op='intersects')
            non_intersecting_gdf = reserve_gdf[~reserve_gdf.index.isin(intersecting_gdf.index)]
            print(non_intersecting_gdf.columns)
            non_intersecting_gdf = non_intersecting_gdf.drop(columns=[ 'loc_desig','terr_mar', 'gis_source', 'notes'])
            non_intersecting_gdf = non_intersecting_gdf.rename(columns={
                "names": "Nombre",
                "mgmt": "Manejador",
                "ownership": "Dueño",
                "year_estab": "Año establecida"
            })
            return non_intersecting_gdf.to_json()
    

    def _foo(gdf):
        return 