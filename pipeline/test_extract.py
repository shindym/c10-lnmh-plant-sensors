"""This file contains tests for the extract functions."""

import re

from extract import get_single_plant_data, extract_relevant_data


def test_get_single_plant_data_returns_dict_for_valid_id(requests_mock):
    """Tests that `get_single_plant_data` returns a dictionary when given a valid plant ID."""

    universal_regex_pattern = re.compile(r".+")

    requests_mock.get(universal_regex_pattern, json={"plant_id": "8"})

    result = get_single_plant_data(8)

    assert isinstance(result, dict)
    assert result['plant_id'] == "8"


def test_get_single_plant_data_nonexistent_returns_none(requests_mock):
    """
    Tests that `get_single_plant_data` returns None when a 404 status is encountered
    for a non-existent plant ID, simulating an API response with a JSON error message.
    """

    error_response = {"error": "Plant not found"}

    requests_mock.get("https://data-eng-plants-api.herokuapp.com/plants/999",
                      json=error_response,
                      status_code=404)

    result = get_single_plant_data(999)

    assert result is None


def test_extract_relevant_data_success():
    """Tests that `get_single_plant_data` extracts all relevant data is correctly from a dictionary."""

    full_plant_data = {
        "plant_id": 1,
        "botanist": {
            "name": "Eliza Andrews",
            "email": "eliza.andrews@lnhm.co.uk",
            "phone": "123-456-7890"
        },
        "last_watered": "2024-04-10",
        "name": "Bird of paradise",
        "origin_location": ["Latitude", "Longitude", "Area", "Country", "Timezone"],
        "recording_taken": "2024-04-15",
        "soil_moisture": 77,
        "temperature": 15,
    }

    result = extract_relevant_data(full_plant_data)

    expected_result = {
        "plant_id": 1,
        "botanist_name": "Eliza Andrews",
        "botanist_email": "eliza.andrews@lnhm.co.uk",
        "botanist_phone": "123-456-7890",
        "last_watered": "2024-04-10",
        "plant_name": "Bird of paradise",
        "origin": "Area",
        "recording_taken": "2024-04-15",
        "soil_moisture": 77,
        "temperature": 15,
    }

    assert result == expected_result, "Extracted data does not match the expected result."


def test_missing_botanist_details():
    """Tests that `get_single_plant_data` handles missing botanist details by returning None for each key."""

    full_plant_data = {
        "plant_id": 1,
        "last_watered": "2024-04-10",
        "name": "Bird of paradise",
        "origin_location": ["Latitude", "Longitude", "Area", "Country", "Timezone"],
        "recording_taken": "2024-04-15",
        "soil_moisture": 96,
        "temperature": 11,
    }

    result = extract_relevant_data(full_plant_data)

    assert result['botanist_name'] is None
    assert result['botanist_email'] is None
    assert result['botanist_phone'] is None


def test_input_none_returns_none():
    """Tests that `get_single_plant_data` handles None input by returning None."""

    result = extract_relevant_data(None)

    assert result is None
