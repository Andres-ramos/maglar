from arcgis.gis import GIS, Item
from arcgis.mapping import WebMap
from arcgis.features import FeatureLayer, FeatureSet

from typing import List, Dict, Any
import json 

from pathlib import Path
#Layer stuff 

#TODO: Figure out what is being used and what isn't
#Create stuff
def write_layer(
        local_layer_file_path:str, 
        geojson: str
    ) -> None:
    """
    Helper function
    Writes geojson to local file
    """
    try :
        with open(str(local_layer_file_path), 'w') as f:
            f.write(geojson)
    except :
        raise Exception("Failed to write layer file")

def upload_layer(
        gis: GIS, 
        layer_title_name:str, 
        local_layer_file_path:Path, 
        storage_folder:str
    ) -> Item:
    """
    Uploads geojson layer to arcgis online
    """
    try :
        item = gis.content.add(
            {
                "title": layer_title_name, 
                "description": "layer-upload test ", 
                "tags": "parcels",
                "type": "GeoJson"
            },
            str(local_layer_file_path),
            folder = storage_folder
        )

        return item.publish()
    except Exception:
        raise Exception("Arcgis layer upload exception")
        
def create_layer(
        gis: GIS, 
        local_layer_file_path:str, 
        geojson:str, 
        layer_title_name:str, 
        storage_folder:str
    ) -> Item:
    """
    Main create function. Uploads layer to arcgis online
    """
    write_layer(local_layer_file_path, geojson)
    return upload_layer(
        gis, 
        layer_title_name, 
        local_layer_file_path, 
        storage_folder
    )



#Update stuff
def get_layer(layer_list: List[Item]) -> Item:
    """
    Helper function
    From a list of possible layer candidates, it picks the feature service
    """
    for layer in layer_list:
        if layer.type == "Feature Service":
            return layer


#TODO: Geojson should only be new features
def update_layer(layer_item, geojson: str) -> None:
    """
    Main Function
    Updates a layer already in arcgis online
    """
    # layer_item = get_layer(layers_item_list)
    f = FeatureLayer.fromitem(layer_item)
    f.append(upsert=True)
    # geojson_dict = json.loads(geojson)
    # updated_features = FeatureSet.from_geojson(geojson_dict)
    # try :
    #     f = FeatureLayer.fromitem(layer_item)
    #     f.edit_features(adds=updated_features)
    #     return f
    # except Exception:
    #     raise Exception("Arcgis update error")


### Webmap stuff

#Create webmap 
def create_webmap_properties(webmap_title_name:str) -> Dict[str, Any]:
    """
    Helper function
    Creates web map properties dictionary
    """
    return {
        'title':webmap_title_name,
        'snippet': "Denuncias de construcciones en la costa",
        'tags': ["python"],
        'extent': {
            'xmin': -67.35397048193602, 
            'ymin': 17.80754468951328, 
            'xmax': -65.11851750203257, 
            'ymax': 18.568671638862668, 
            'spatialReference': {'wkid': 4326}
        }
    }


def create_style(color):
    outline_color = [0, 0, 0, 255]
    outline_width = 0.75
    color_map = {
        "red": [255, 0, 0, 100],
        "green": [0,255,0,100],
        "blue": [0,0,255,100]
    }
    rgba_color = color_map[color]

    return {"renderer": {
        'type': 'simple', 
        'symbol': {
            'type': 'esriSFS', 
            'style': 'esriSFSSolid', 
            'color': rgba_color, 
            'outline': {
                'type': 'esriSLS', 
                'style': 'esriSLSSolid', 
                'color': outline_color, 
                'width': outline_width
                }
            }
        }
    }

def create_map(
        webmap_title_name:str, 
        storage_folder:str
    )-> None:
    """
    Main function
    Creates webmap with given layer list and uploads to arcgis
    """
    #Create webmap
    wm = WebMap()
    #Creates webmap properties
    webmap_item_properties = create_webmap_properties(webmap_title_name)
    #Saves webmap item 
    try :
        new_wm_item = wm.save(
            webmap_item_properties, 
            folder=storage_folder
        )
        wm = WebMap(new_wm_item)
        wm.basemap.baseMapLayers = [
            {
                "id": "VectorTile_1970",
                "opacity": 1,
                "title": "Base gris clara",
                "visibility": True,
                "layerType": "VectorTileLayer",
                "styleUrl": "https://cdn.arcgis.com/sharing/rest/content/items/ae7c8edcad024c4faa73368f3c5e358d/resources/styles/root.json"
            },
            {
                "id": "VectorTile_7117",
                "opacity": 1,
                "title": "Referencia gris clara",
                "visibility": True,
                "layerType": "VectorTileLayer",
                "styleUrl": "https://cdn.arcgis.com/sharing/rest/content/items/a55e1825605f49599a09b73e59f5526a/resources/styles/root.json",
                "isReference": True
            }
        ]
        return wm
    except Exception:
        raise Exception("Arcgis web map creation error")

def find_webmap(p_webmaps, webmap_title_name):
    if len(p_webmaps) == 0:
        wm = None
    #Find webmap
    elif len(p_webmaps) == 1 :
        wm = WebMap(p_webmaps[0])
    else :
        wm = None
        for p_webmap in p_webmaps:
            if p_webmap.title == webmap_title_name and p_webmap.type == "Web Map":
                wm = WebMap(p_webmap)
    return wm

