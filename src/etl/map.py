from typing import Any
from typing import Dict

from arcgis.mapping import WebMap


# Create webmap
def create_webmap_properties(webmap_title_name: str) -> Dict[str, Any]:
    """
    Helper function
    Creates web map properties dictionary
    """
    return {
        "title": webmap_title_name,
        "snippet": "Denuncias de construcciones en la costa",
        "tags": ["python"],
        "extent": {
            "xmin": -67.35397048193602,
            "ymin": 17.80754468951328,
            "xmax": -65.11851750203257,
            "ymax": 18.568671638862668,
            "spatialReference": {"wkid": 4326},
        },
    }


def create_map(webmap_title_name: str, storage_folder: str) -> None:
    """
    Main function
    Creates webmap with given layer list and uploads to arcgis
    """
    # Create webmap
    wm = WebMap()
    # Creates webmap properties
    webmap_item_properties = create_webmap_properties(webmap_title_name)
    # Saves webmap item
    try:
        new_wm_item = wm.save(webmap_item_properties, folder=storage_folder)
        wm = WebMap(new_wm_item)
        wm.basemap.baseMapLayers = [
            {
                "id": "VectorTile_1970",
                "opacity": 1,
                "title": "Base gris clara",
                "visibility": True,
                "layerType": "VectorTileLayer",
                "styleUrl": "https://cdn.arcgis.com/sharing/rest/content/items/ae7c8edcad024c4faa73368f3c5e358d/resources/styles/root.json",  # noqa
            },
            {
                "id": "VectorTile_7117",
                "opacity": 1,
                "title": "Referencia gris clara",
                "visibility": True,
                "layerType": "VectorTileLayer",
                "styleUrl": "https://cdn.arcgis.com/sharing/rest/content/items/a55e1825605f49599a09b73e59f5526a/resources/styles/root.json",  # noqa
                "isReference": True,
            },
        ]
        return wm
    except Exception:
        raise Exception("Arcgis web map creation error")
