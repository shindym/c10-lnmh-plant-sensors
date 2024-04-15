"""This file is responsible for extracting data from the plant sensor API"""
import requests


def get_single_plant_data(plant_id: int) -> dict:
    """
    Contacts the api and uses the given plant_id to get to a specific endpoint.
    Returns the json data.
    """

    response = requests.get(
        f"https://data-eng-plants-api.herokuapp.com/plants/{plant_id}", timeout=10)

    return response.json()


if __name__ == "__main__":
    p = get_single_plant_data(8)
    print(p)
