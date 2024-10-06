import geopandas as gpd
def generate_report_layer(gdf):
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