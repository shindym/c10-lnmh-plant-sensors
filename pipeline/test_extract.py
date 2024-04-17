"""This file contains tests for the extract functions."""

import re

from extract import get_single_plant_data, extract_relevant_data


def test_valid_plant_id_returns_dict(requests_mock):
    """
    Tests that `get_single_plant_data` returns a dictionary when given a valid plant ID.
    """

    any_url_pattern = re.compile(r".+")

    requests_mock.get(any_url_pattern, json={"plant_id": "8"})

    result = get_single_plant_data(8)

    assert isinstance(result, dict)
    assert result['plant_id'] == "8"


def test_nonexistent_plant_id_returns_none(requests_mock):
    """
    Tests that `get_single_plant_data` returns None when a 404 status is encountered
    for a non-existent plant ID, simulating an API response with a JSON error message.
    """

    any_url_pattern = re.compile(r".+")

    error_response = {"error": "Plant not found"}

    requests_mock.get(any_url_pattern, json=error_response, status_code=404)

    result = get_single_plant_data(999)

    assert result is None


def test_extracts_relevant_data_successfully():
    """
    Tests that `extract_relevant_data` extracts all relevant data correctly from a dictionary.
    """

    full_plant_data = {
        "plant_id": 1,
        "botanist": {
            "name": "Eliza Andrews",
            "email": "eliza.andrews@lnhm.co.uk",
            "phone": "123-456-7890"
        },
        "last_watered": "2024-04-10",
        "name": "Bird of paradise",
        "scientific_name": ['Heliconia schiedeana "Fire and Ice"'],
        "origin_location": ["Latitude", "Longitude", "Area", "Country", "Timezone"],
        "recording_taken": "2024-04-15",
        "soil_moisture": 77,
        "temperature": 15,
    }

    expected_result = {
        "plant_id": 1,
        "botanist_name": "Eliza Andrews",
        "botanist_email": "eliza.andrews@lnhm.co.uk",
        "botanist_phone": "123-456-7890",
        "last_watered": "2024-04-10",
        "plant_common_name": "Bird of paradise",
        "plant_scientific_name": 'Heliconia schiedeana "Fire and Ice"',
        "origin_area": "Area",
        "origin_latitude": "Latitude",
        "origin_longitude": "Longitude",
        "recording_taken": "2024-04-15",
        "soil_moisture": 77,
        "temperature": 15,
    }

    result = extract_relevant_data(full_plant_data)

    assert result == expected_result


def test_missing_botanist_details():
    """
    Tests that `extract_relevant_data` handles missing botanist details by returning None for each key.
    """

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


def test_none_input_returns_none():
    """
    Tests that `extract_relevant_data` handles None input by returning None.
    """

    result = extract_relevant_data(None)

    assert result is None
