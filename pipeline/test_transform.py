"""This file contains tests for the transform functions."""

import pandas as pd
import pytest

from transform import extract_first_name_last_name, clean_data


def test_extract_valid_first_and_last_name():
    """
    Tests that `extract_first_name_last_name` extracts the first
    and last name correctly and drops the original full_name column.
    """

    df = pd.DataFrame({
        "botanist_name": ["Gertrude Jekyll", "Eliza Andrews"]
    })

    resulting_df = extract_first_name_last_name(df)

    assert resulting_df["botanist_first_name"].tolist() == ["Gertrude", "Eliza"]

    assert resulting_df["botanist_last_name"].tolist() == ["Jekyll", "Andrews"]

    assert "botanist_name" not in resulting_df.columns


def test_clean_data_handles_nonexistent_file():
    """
    Tests that `clean_data` raises a FileNotFoundError when the file does not exist.
    """

    with pytest.raises(FileNotFoundError):
        clean_data("non_existent_file.csv")


def test_data_is_cleaned_correctly(tmpdir):
    """
    Tests that `clean_data` removes rows with invalid soil moisture
    and temperature values and converts botanist columns to strings.
    """

    # Creates temporary subdirectory and file
    subdirectory = tmpdir.mkdir("sub")
    csv_file_path = str(subdirectory.join("test_file.csv"))

    test_data = {
        "botanist_name": ["Gertrude Jekyll", "Bob Johnson"],
        "soil_moisture": [10, 30],
        "temperature": [5, 25],
        "botanist_email": ["gertrude.jekyll@lnhm.co.uk", "eliza.andrews@lnhm.co.uk"],
        "botanist_phone": ["123", "456"],
        "last_watered": ["2024-01-01", "2024-01-02"],
        "plant_common_name": ["Daisy", "Rose"],
        "plant_scientific_name": ["Bellis Perennis", "Rosa"],
        "origin_area": ["Europe", "Asia"],
        "recording_taken": ["2024-01-01 12:00:00", "2024-01-02 12:00:00"]
    }

    # Creates dataframe from the test data
    pd.DataFrame(test_data).to_csv(csv_file_path, index=False)

    clean_data(csv_file_path)

    # Reading back the cleaned data
    cleaned_df = pd.read_csv(csv_file_path)

    assert len(cleaned_df) == 2
    assert cleaned_df['soil_moisture'].iloc[0] > 0 and cleaned_df['soil_moisture'].iloc[0] < 100
    assert cleaned_df['temperature'].iloc[0] > 0 and cleaned_df['temperature'].iloc[0] < 50
    assert pd.api.types.is_string_dtype(cleaned_df['botanist_first_name'])
