from typing import List

import requests
from requests.auth import HTTPBasicAuth

from ..logger import logger


def fetch_with_radius(points: List, url: str, radius: int, auth: HTTPBasicAuth) -> List:
    record_list = []
    for point in points:
        logger.info(f"Fetching from {url}")
        point_str = f"{point.x},{point.y}"
        params = {"dist": radius, "point": point_str}
        pitirre_response = requests.get(url, auth=auth, params=params)
        pitirre_result = pitirre_response.json()
        record_list += pitirre_result["results"]["features"]

    return record_list
