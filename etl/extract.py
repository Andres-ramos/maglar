from arcgis.gis import GIS, ContentManager
from arcgis.apps.survey123 import SurveyManager
import geopandas as gpd 

def download_survey_data(
        survey_id:str,
        content_manager:ContentManager, 
        survey_manager:SurveyManager, 
        download_path='survey_data'
    ) -> str:
    """
    Receives survey manager, content manager and survey_id
    downloads survey data into download path
    Returns - download path
    """
    survey_item = content_manager.get(survey_id)
    survey_obj = survey_manager.get(survey_item.id)
    path = survey_obj.download(export_format="Shapefile", save_folder=download_path)
    return path


def extract(survey_id, survey_manager, content_manager):

    #TODO: Hacer try-catch
    # for survey in survey_manager.surveys:
    #     if survey.properties["title"] == survey_title:
    #         survey_id = survey.properties["id"]
    
    path = download_survey_data(survey_id, content_manager, survey_manager)
    return gpd.read_file(path)