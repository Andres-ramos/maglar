from ..layer import Layer


class ClusterLayer(Layer):
    def __init__(self, gis, layer_title, arcgis_storage_folder):
        super().__init__(gis, layer_title, arcgis_storage_folder)

    def generate_layer_geojson(self, gdf):
        # Extract rows that have multiple construccion column
        f_gdf = gdf[gdf["_hay_otras"] == "Si"]
        f_gdf = f_gdf.drop(
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
        f_gdf = f_gdf.rename(
            columns={
                "_qu_ves_ti": "¿Qué ves? Tipo de observación",
                "pueblo_en_": "Pueblo",
                "_hay_otras": "¿Hay otras observaciones aledañas al lugar?",
                "_se_pudo_o": "¿Qué otras observaciones viste?",
            }
        )

        return f_gdf.to_json()

    def generate_style(self):
        return {
            "renderer": {
                "type": "simple",
                "symbol": {
                    "type": "CIMSymbolReference",
                    "symbol": {
                        "type": "CIMPointSymbol",
                        "symbolLayers": [
                            {
                                "type": "CIMVectorMarker",
                                "enable": True,
                                "anchorPoint": {"x": 0, "y": 0},
                                "anchorPointUnits": "Relative",
                                "dominantSizeAxis3D": "Y",
                                "size": 18.75,
                                "billboardMode3D": "FaceNearPlane",
                                "frame": {
                                    "xmin": -300,
                                    "ymin": -300,
                                    "xmax": 300,
                                    "ymax": 300,
                                },
                                "markerGraphics": [
                                    {
                                        "type": "CIMMarkerGraphic",
                                        "geometry": {
                                            "rings": [
                                                [
                                                    [12, 121],
                                                    [24, 119],
                                                    [36, 116],
                                                    [47, 112],
                                                    [58, 107],
                                                    [68, 101],
                                                    [77, 94],
                                                    [86, 86],
                                                    [94, 77],
                                                    [101, 68],
                                                    [107, 58],
                                                    [112, 47],
                                                    [116, 36],
                                                    [119, 24],
                                                    [121, 12],
                                                    [122, 0],
                                                    [121, -12],
                                                    [119, -24],
                                                    [116, -36],
                                                    [112, -47],
                                                    [107, -58],
                                                    [101, -68],
                                                    [94, -77],
                                                    [86, -86],
                                                    [77, -94],
                                                    [68, -101],
                                                    [58, -107],
                                                    [47, -112],
                                                    [36, -116],
                                                    [24, -119],
                                                    [12, -121],
                                                    [0, -122],
                                                    [-12, -121],
                                                    [-24, -119],
                                                    [-36, -116],
                                                    [-47, -112],
                                                    [-58, -107],
                                                    [-68, -101],
                                                    [-77, -94],
                                                    [-86, -86],
                                                    [-94, -77],
                                                    [-101, -68],
                                                    [-107, -58],
                                                    [-112, -47],
                                                    [-116, -36],
                                                    [-119, -24],
                                                    [-121, -12],
                                                    [-122, 0],
                                                    [-121, 12],
                                                    [-119, 24],
                                                    [-116, 36],
                                                    [-112, 47],
                                                    [-107, 58],
                                                    [-101, 68],
                                                    [-94, 77],
                                                    [-86, 86],
                                                    [-77, 94],
                                                    [-68, 101],
                                                    [-58, 107],
                                                    [-47, 112],
                                                    [-36, 116],
                                                    [-24, 119],
                                                    [-12, 121],
                                                    [0, 122],
                                                    [12, 121],
                                                ],
                                                [
                                                    [-17, 171],
                                                    [-34, 169],
                                                    [-51, 165],
                                                    [-67, 159],
                                                    [-82, 151],
                                                    [-96, 143],
                                                    [-110, 133],
                                                    [-122, 122],
                                                    [-133, 110],
                                                    [-143, 96],
                                                    [-151, 82],
                                                    [-159, 67],
                                                    [-165, 51],
                                                    [-169, 34],
                                                    [-171, 17],
                                                    [-172, 0],
                                                    [-171, -17],
                                                    [-169, -34],
                                                    [-165, -51],
                                                    [-159, -67],
                                                    [-151, -82],
                                                    [-143, -96],
                                                    [-133, -110],
                                                    [-122, -122],
                                                    [-110, -133],
                                                    [-96, -143],
                                                    [-82, -151],
                                                    [-67, -159],
                                                    [-51, -165],
                                                    [-34, -169],
                                                    [-17, -171],
                                                    [0, -172],
                                                    [17, -171],
                                                    [34, -169],
                                                    [51, -165],
                                                    [67, -159],
                                                    [82, -151],
                                                    [96, -143],
                                                    [110, -133],
                                                    [122, -122],
                                                    [133, -110],
                                                    [143, -96],
                                                    [151, -82],
                                                    [159, -67],
                                                    [165, -51],
                                                    [169, -34],
                                                    [171, -17],
                                                    [172, 0],
                                                    [171, 17],
                                                    [169, 34],
                                                    [165, 51],
                                                    [159, 67],
                                                    [151, 82],
                                                    [143, 96],
                                                    [133, 110],
                                                    [122, 122],
                                                    [110, 133],
                                                    [96, 143],
                                                    [82, 151],
                                                    [67, 159],
                                                    [51, 165],
                                                    [34, 169],
                                                    [17, 171],
                                                    [0, 172],
                                                    [-17, 171],
                                                ],
                                                [
                                                    [11, 210],
                                                    [21, 209],
                                                    [32, 208],
                                                    [42, 206],
                                                    [52, 204],
                                                    [62, 201],
                                                    [72, 197],
                                                    [82, 194],
                                                    [100, 184],
                                                    [118, 174],
                                                    [134, 162],
                                                    [148, 148],
                                                    [162, 134],
                                                    [174, 118],
                                                    [184, 100],
                                                    [194, 82],
                                                    [197, 72],
                                                    [201, 62],
                                                    [204, 52],
                                                    [206, 42],
                                                    [208, 32],
                                                    [209, 21],
                                                    [210, 11],
                                                    [210, 0],
                                                    [210, -11],
                                                    [209, -21],
                                                    [208, -32],
                                                    [206, -42],
                                                    [204, -52],
                                                    [201, -62],
                                                    [197, -72],
                                                    [194, -82],
                                                    [184, -100],
                                                    [174, -118],
                                                    [162, -134],
                                                    [148, -148],
                                                    [134, -162],
                                                    [118, -174],
                                                    [100, -184],
                                                    [82, -194],
                                                    [72, -197],
                                                    [62, -201],
                                                    [52, -204],
                                                    [42, -206],
                                                    [32, -208],
                                                    [21, -209],
                                                    [11, -210],
                                                    [0, -210],
                                                    [-11, -210],
                                                    [-21, -209],
                                                    [-32, -208],
                                                    [-42, -206],
                                                    [-52, -204],
                                                    [-62, -201],
                                                    [-72, -197],
                                                    [-82, -194],
                                                    [-100, -184],
                                                    [-118, -174],
                                                    [-134, -162],
                                                    [-148, -148],
                                                    [-162, -134],
                                                    [-174, -118],
                                                    [-184, -100],
                                                    [-194, -82],
                                                    [-197, -72],
                                                    [-201, -62],
                                                    [-204, -52],
                                                    [-206, -42],
                                                    [-208, -32],
                                                    [-209, -21],
                                                    [-210, -11],
                                                    [-210, 0],
                                                    [-210, 11],
                                                    [-209, 21],
                                                    [-208, 32],
                                                    [-206, 42],
                                                    [-204, 52],
                                                    [-201, 62],
                                                    [-197, 72],
                                                    [-194, 82],
                                                    [-184, 100],
                                                    [-174, 118],
                                                    [-162, 134],
                                                    [-148, 148],
                                                    [-134, 162],
                                                    [-118, 174],
                                                    [-100, 184],
                                                    [-82, 194],
                                                    [-72, 197],
                                                    [-62, 201],
                                                    [-52, 204],
                                                    [-42, 206],
                                                    [-32, 208],
                                                    [-21, 209],
                                                    [-11, 210],
                                                    [0, 210],
                                                    [11, 210],
                                                ],
                                            ]
                                        },
                                        "symbol": {
                                            "type": "CIMPolygonSymbol",
                                            "symbolLayers": [
                                                {
                                                    "type": "CIMSolidStroke",
                                                    "enable": True,
                                                    "capStyle": "Round",
                                                    "joinStyle": "Round",
                                                    "lineStyle3D": "Strip",
                                                    "miterLimit": 10,
                                                    "width": 0.375,
                                                    "color": [0, 0, 128, 217],
                                                },
                                                {
                                                    "type": "CIMSolidFill",
                                                    "enable": True,
                                                    "color": [249, 233, 0, 255],
                                                },
                                            ],
                                            "angleAlignment": "Map",
                                        },
                                    }
                                ],
                                "respectFrame": True,
                                "rotation": 360,
                            }
                        ],
                        "haloSize": 1,
                        "scaleX": 1,
                        "angleAlignment": "Display",
                        "angle": 360,
                    },
                },
            }
        }
