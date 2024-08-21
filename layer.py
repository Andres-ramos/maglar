from typing import List, Any
import json
from arcgis.gis import GIS, Item
from pathlib import Path
from arcgis.features import FeatureLayer, FeatureSet




class Layer:
    def __init__(self, gis, layer_title, arcgis_storage_folder):
        self.gis = gis
        self.layer_title = layer_title
        self.file_path = self._generate_file_path()
        self.layer_item = self._get_layer_item(layer_title)
        print(self.layer_item)
        self.arcgis_storage_folder = arcgis_storage_folder
        self.layer_style = None

    def _generate_file_path(self):
        return f"./geojson_data/{self.layer_title}.geojson"
    
    def _get_layer_item(self, layer_title):
        p_layers = self.gis.content.search(layer_title)
        return self._find_layer(possible_layers_list=p_layers)
    
    def _find_layer(self, possible_layers_list: List[Any]):
    
        for p_layer_item in possible_layers_list:
            if p_layer_item.title == p_layer_item["title"] and p_layer_item.type == "Feature Service":
                return p_layer_item
        return None
    
    def update_or_create(self, wm, geojson):

        # If no layer with title name have been created, create layer and update map
        if self.layer_item == None:
            print("creating layer", self.layer_title)
            #If geojson has no features don't upload layer
            if len(json.loads(geojson)["features"]) > 0:
                layer_item = self._create_layer(
                    self.gis,
                    self.file_path,
                    geojson,
                    self.layer_title,
                    self.arcgis_storage_folder
                )
                self.layer_item = layer_item
                return "create"


        #If layer and webmaps have already been created, update layer map updates automatically
        else :
            #Supone que no se remueven features del anterior
            # Se pasan solo las que se anadieron
            # 
            layer_item = self._update_layer(geojson)
            return "update"
        return 
    
    def _create_layer(
        self,
        gis: GIS, 
        local_layer_file_path:str, 
        geojson:str, 
        layer_title_name:str, 
        storage_folder:str
        ) -> Item:
        """
        Main create function. Uploads layer to arcgis online
        """
        self._write_layer(local_layer_file_path, geojson)
        return self._upload_layer(
            gis, 
            layer_title_name, 
            local_layer_file_path, 
            storage_folder
        )
    

    #Create stuff
    def _write_layer(
            self,
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

    def _upload_layer(
            self,
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
    
    #TODO: Geojson should only be new features
    def _update_layer(self, geojson: str) -> None:
        """
        Main Function
        Updates a layer already in arcgis online
        """
        geojson_dict = json.loads(geojson)
        updated_features = FeatureSet.from_geojson(geojson_dict)
        try :
            f = FeatureLayer.fromitem(self.layer_item)
            f.edit_features(adds=updated_features)
            return f
        except Exception:
            raise Exception("Arcgis update error")
