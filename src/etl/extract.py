import tempfile

import geopandas as gpd
import pandas as pd
from arcgis.apps.survey123 import SurveyManager
from arcgis.gis import ContentManager


def download_survey_data(
    survey_id: str, survey_manager: SurveyManager, content_manager: ContentManager
) -> str:
    """
    Receives survey manager, content manager and survey_id
    downloads survey data into download path
    Returns - download path
    """
    temp_dir = tempfile.TemporaryDirectory().name
    survey_item = content_manager.get(survey_id)
    # test_woo =
    # print(survey_item.layers)
    # survey_feature_layer = content_manager.get(test_woo)
    # survey_layer = survey_feature_layer.layers[0]
    # print()
    survey_obj = survey_manager.get(survey_item.id)
    path = survey_obj.download(export_format="CSV", save_folder=temp_dir)
    return path


def extract(
    survey_id: str, survey_manager: SurveyManager, content_manager: ContentManager
) -> gpd.GeoDataFrame:
    try:
        path = download_survey_data(survey_id, survey_manager, content_manager)
        return pd.read_csv(path)

    except Exception:
        raise Exception("Failed to download survey")
