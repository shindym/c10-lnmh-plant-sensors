"""This file is responsible for extracting data from the plant sensor API"""
import requests


def get_single_plant_data(plant_id: int) -> dict:
    """
    Contacts the api and uses the given plant_id to get to a specific endpoint.
    Returns the json data.
    """

    try:
        response = requests.get(
            f"https://data-eng-plants-api.herokuapp.com/plants/{plant_id}", timeout=10)
    except requests.exceptions.ReadTimeout:
        return None

    json_data = response.json()

    if "error" in json_data:
        return None

    return json_data


def get_all_plant_data():
    total_plants = 50
    plants = []

    for i in range(0, total_plants):
        print(i)
        plants.append(get_single_plant_data(i))


if __name__ == "__main__":
    get_all_plant_data()
