from arcgis.gis import GIS, ContentManager, Item
from arcgis.mapping import WebMap
from arcgis.features import FeatureLayer, FeatureSet

from typing import List, Dict, Any
import json 


#Layer stuff 

#Create stuff
def write_layer(
        layer_file_name:str, 
        geojson: str
    ) -> None:
    """
    Helper function
    Writes geojson to local file
    """
    try :
        with open(layer_file_name, 'w') as f:
            f.write(geojson)
    except :
        raise Exception("Failed to write layer file")

def upload_layer(
        gis: GIS, 
        layer_title_name:str, 
        layer_file_name:str, 
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
            layer_file_name,
            folder = storage_folder
        )

        return item.publish()
    except Exception:
        raise Exception("Arcgis layer upload exception")
        
def create_layer(
        gis: GIS, 
        layer_file_name:str, 
        geojson:str, 
        layer_title_name:str, 
        storage_folder:str
    ) -> Item:
    """
    Main create function. Uploads layer to arcgis online
    """
    write_layer(layer_file_name, geojson)
    return upload_layer(
        gis, 
        layer_title_name, 
        layer_file_name, 
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


def update_layer(layers_item_list: List[Any], geojson: str) -> None:
    """
    Main Function
    Updates a layer already in arcgis online
    """
    layer_item = get_layer(layers_item_list)
    geojson_dict = json.loads(geojson)
    updated_features = FeatureSet.from_geojson(geojson_dict)
    try :
        f = FeatureLayer.fromitem(layer_item)
        f.edit_features(adds=updated_features)
        return 
    except Exception:
        raise Exception("Arcgis update error")


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

def create_map(
        webmap_title_name:str, 
        layers:List[Any], 
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
    #Add layers to map 
    wm.add_layer(layers[0])
    # wm.add_layer(protected_area)

    #Saves webmap item 
    try :
        new_wm_item = wm.save(
            webmap_item_properties, 
            folder=storage_folder
        )
        return new_wm_item
    except Exception:
        raise Exception("Arcgis web map creation error")