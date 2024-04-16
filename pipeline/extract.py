"""This file is responsible for extracting data from the plant sensor API"""
import requests
import pandas as pd


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

    if "error" in json_data or "plant_id" not in json_data:
        return None

    return json_data


def extract_relevant_data(full_plant_data: dict):
    if full_plant_data is None:
        return None

    filtered_plant_data = {}

    filtered_plant_data["plant_id"] = full_plant_data["plant_id"]
    filtered_plant_data["botanist_name"] = full_plant_data.get(
        "botanist", {"name": None})["name"]
    filtered_plant_data["botanist_email"] = full_plant_data.get(
        "botanist", {"email": None})["email"]
    filtered_plant_data["botanist_phone"] = full_plant_data.get(
        "botanist", {"phone": None})["phone"]
    filtered_plant_data["last_watered"] = full_plant_data.get(
        "last_watered", None)
    filtered_plant_data["plant_name"] = full_plant_data.get("name", None)
    filtered_plant_data["recording_taken"] = full_plant_data.get(
        "recording_taken", None)
    filtered_plant_data["soil_moisture"] = full_plant_data.get(
        "soil_moisture", None)
    filtered_plant_data["temperature"] = full_plant_data.get(
        "temperature", None)

    return filtered_plant_data


def get_all_plant_data():
    total_plants = 50
    plants = []

    for i in range(0, total_plants+1):
        plant = extract_relevant_data(get_single_plant_data(i))
        if plant is not None:
            plants.append(plant)

    return plants


if __name__ == "__main__":
    df = pd.DataFrame(get_all_plant_data())
    df.to_csv("plant_data.csv", index=False)
