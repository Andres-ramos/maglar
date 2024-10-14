import requests


def query_pitirre(row):
    # num_records = 10
    url = "http://127.0.0.1:8000/parcels/"

    x, y = row.x, row.y
    # x,y = -67.16076297678497, 18.450717761715765
    params = {"point": f"{x},{y}", "dist": 15}

    # TODO: Get authorization from env file
    headers = {"Authorization": "Basic YWRtaW46MTIzNA=="}

    response = requests.get(url, params=params, headers=headers)

    return response.json()["results"]
