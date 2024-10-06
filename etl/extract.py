from arcgis.gis import GIS, ContentManager
from arcgis.apps.survey123 import SurveyManager
import geopandas as gpd 
import tempfile

#TODO: Document file

def download_survey_data(
        survey_id:str,
        content_manager:ContentManager, 
        survey_manager:SurveyManager, 
    ) -> str:
    """
    Receives survey manager, content manager and survey_id
    downloads survey data into download path
    Returns - download path
    """
    temp_dir = tempfile.TemporaryDirectory().name
    survey_item = content_manager.get(survey_id)
    survey_obj = survey_manager.get(survey_item.id)
    path = survey_obj.download(export_format="Shapefile", save_folder=temp_dir)
    return path


def extract(survey_id, survey_manager, content_manager):
    try :
        path = download_survey_data(survey_id, content_manager, survey_manager)
        return gpd.read_file(path)
    except Exception:
        raise Exception("Failed to download survey")