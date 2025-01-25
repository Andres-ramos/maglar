import geopandas as gpd
from shapely.geometry import Polygon

# TODO: Document file
PR_AOI = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "coordinates": [
                    [
                        [-67.35397048193602, 18.568671638862668],
                        [-67.35397048193602, 17.80754468951328],
                        [-65.11851750203257, 17.80754468951328],
                        [-65.11851750203257, 18.568671638862668],
                        [-67.35397048193602, 18.568671638862668],
                    ]
                ],
                "type": "Polygon",
            },
        }
    ],
}


def filter_data(gdf):
    # spatial filter
    aoi_coords = PR_AOI["features"][0]["geometry"]["coordinates"][0]
    polygon = Polygon(aoi_coords)
    aoi_gdf = gpd.GeoDataFrame(index=[0], crs=4326, geometry=[polygon]).to_crs(4326)
    filtered_gdf = gpd.sjoin(gdf, aoi_gdf, op="within")
    return filtered_gdf
