from typing import List, Any
import json
from arcgis.gis import GIS, Item
from pathlib import Path
from arcgis.features import FeatureLayer, FeatureSet

from arcgis import geometry
from copy import deepcopy
import geopandas as gpd 
from arcgis.features import FeatureLayerCollection


class Layer:
    def __init__(self, gis, layer_title, arcgis_storage_folder, color):
        self.gis = gis
        self.layer_title = layer_title
        self.file_path = self._generate_file_path()
        self.layer_item = self._get_layer_item(layer_title)
        self.arcgis_storage_folder = arcgis_storage_folder
        self.layer_style = self._create_style(color) if color else None

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
    
    def update_or_create(self, geojson):
        print("update_or_create", self.layer_title)
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
            if len(json.loads(geojson)["features"]) > 0:
                if self.layer_title == "report_layer":

                    # layer_item = self._update_layer(geojson)
                    fe_collection = FeatureLayerCollection.fromitem(self.layer_item)
                    with open(self.file_path, 'w') as f:
                        f.write(geojson)

                    fe_collection.manager.overwrite(self.file_path)
                    return "update"

                elif self.layer_title == "over_reservation_layer":

                    fe_collection = FeatureLayerCollection.fromitem(self.layer_item)
                    with open(self.file_path, 'w') as f:
                        f.write(geojson)

                    fe_collection.manager.overwrite(self.file_path)
                    return "update"
                elif self.layer_title == "non_overlap_reservation_layer":
                  
                    fe_collection = FeatureLayerCollection.fromitem(self.layer_item)
                    with open(self.file_path, 'w') as f:
                        f.write(geojson)

                    fe_collection.manager.overwrite(self.file_path)

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
        print("_create_layer")
        self._write_layer(local_layer_file_path, geojson)
        try :
            return self._upload_layer(
                gis, 
                layer_title_name, 
                local_layer_file_path, 
                storage_folder
            )
        except Exception:
            raise("Failed to upload layer")
    

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
                data=str(local_layer_file_path),
                folder = storage_folder
            )
            print("item to publish", item)
            return item.publish()
        except Exception as e:
            print(e)
            raise Exception("Arcgis layer upload exception")
    
    #TODO: Geojson should only be new features
    def _update_layer(self, geojson: str) -> None:
        """
        Main Function
        Updates a layer already in arcgis online
        """
        geojson_dict = json.loads(geojson)
        updated_feature_list = []
        updated_features = FeatureSet.from_geojson(geojson_dict)
        template = updated_features.features[0]
        gdf = updated_features.sdf
        for _, row in gdf.iterrows():
            new_feature = deepcopy(template)
            print(new_feature)
            input_geometry = {'y':float(row['SHAPE']['y']),
                       'x':float(row['SHAPE']['x'])}
            output_geometry = geometry.project(geometries = [input_geometry],
                                    in_sr = 6566, 
                                    out_sr = 6566)
            new_feature.geometry = output_geometry[0]
            new_feature.attributes['¿Qué ves? Tipo de observación'] = row['¿Qué ves? Tipo de observación']
            new_feature.attributes["globalid"] = row["globalid"]
            new_feature.attributes["Pueblo"] = row["Pueblo"]
            new_feature.attributes["¿Hay otras observaciones aledañas al lugar?"] = row["¿Hay otras observaciones aledañas al lugar?"]
            new_feature.attributes["¿Qué otras observaciones viste?"] = row["¿Qué otras observaciones viste?"]
            print(new_feature.attributes)
            updated_feature_list.append(new_feature)
        print("hasya aqui")
        try :
            f = FeatureLayer.fromitem(self.layer_item)
            f.edit_features(adds=updated_feature_list)
        except Exception as e:
            print(e)
            raise Exception("Arcgis update error")

    def _create_style(self,color):
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