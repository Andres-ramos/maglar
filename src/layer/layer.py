import json
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Union

from arcgis.features import FeatureLayerCollection
from arcgis.gis import GIS
from arcgis.gis import Item

from ..constants import LOCAL_STORAGE_FOLDER
from ..logger import logger


# TODO: Programatically create description for layer
class Layer:
    def __init__(self, gis: GIS, layer_title: str, arcgis_storage_folder: str):
        self.gis = gis
        self.layer_title = layer_title
        self.file_path = self._generate_file_path()
        self.layer_item = self._get_layer_item(layer_title)
        self.arcgis_storage_folder = arcgis_storage_folder

    def update_or_create(self, geojson: Dict[str, Any]) -> str:
        """
        Updates or creates layer with data from geojson
        """
        # If no layer with title name have been created, create layer and update map
        if self.layer_item is None:
            # If geojson has no features don't upload layer
            if len(json.loads(geojson)["features"]) > 0:
                layer_item = self._create_layer(
                    self.gis,
                    self.file_path,
                    geojson,
                    self.layer_title,
                    self.arcgis_storage_folder,
                )
                self.layer_item = layer_item
                return "create"

        # If layer and webmaps have already been created,
        # update layer map updates automatically
        if len(json.loads(geojson)["features"]) > 0:
            # Overwrites current geojson file
            fe_collection = FeatureLayerCollection.fromitem(self.layer_item)
            with open(self.file_path, "w") as f:
                f.write(geojson)
            fe_collection.manager.overwrite(self.file_path)
            return "update"

        return

    def _create_layer(
        self,
        gis: GIS,
        local_layer_file_path: str,
        geojson: str,
        layer_title_name: str,
        storage_folder: str,
    ) -> Item:
        """
        Main create function. Uploads layer to arcgis online
        """
        self._write_layer(local_layer_file_path, geojson)
        try:
            return self._upload_layer(
                gis, layer_title_name, local_layer_file_path, storage_folder
            )
        except Exception:
            logger.error(f"Failed to upload layer: {layer_title_name}")
            raise ("Failed to upload layer")

    # Create stuff
    def _write_layer(self, local_layer_file_path: str, geojson: str) -> None:
        """
        Helper function
        Writes geojson to local file
        """
        try:
            with open(str(local_layer_file_path), "w") as f:
                f.write(geojson)
        except Exception:
            logger.error(f"Failed to write layer to path {local_layer_file_path}")
            raise Exception("Failed to write layer file")

    def _upload_layer(
        self,
        gis: GIS,
        layer_title_name: str,
        local_layer_file_path: Path,
        storage_folder: str,
    ) -> Item:
        """
        Uploads geojson layer to arcgis online
        """
        try:
            item = gis.content.add(
                {
                    "title": layer_title_name,
                    "description": "layer-upload test ",
                    "tags": "parcels",
                    "type": "GeoJson",
                },
                data=str(local_layer_file_path),
                folder=storage_folder,
            )
            return item.publish()
        except Exception:
            raise Exception("Arcgis layer upload exception")

    def _generate_file_path(self) -> str:
        """
        Generates path to local geojson file
        """
        return f"./static/{LOCAL_STORAGE_FOLDER}/{self.layer_title}.geojson"

    def _get_layer_item(self, layer_title: str) -> Union(Item, None):
        """
        Looks for layer in arcgis cloud
        """
        p_layers = self.gis.content.search(query=f"title:{layer_title}")
        return self._find_layer(possible_layers_list=p_layers)

    def _find_layer(self, possible_layers_list: List[Any]) -> Union(Item, None):
        for p_layer_item in possible_layers_list:
            if (
                p_layer_item.title == self.layer_title
                and p_layer_item.type == "Feature Service"
            ):
                return p_layer_item
        return None
