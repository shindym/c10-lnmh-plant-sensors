"""This file contains tests for the transform functions."""

import pandas as pd

from transform import extract_first_name_last_name, clean_data, add_botanist_id


def test_extracts_valid_first_and_last_name():
    """Tests that `extract_first_name_last_name` extracts the first
    and last name correctly and drops the original column."""

    df = pd.DataFrame({
        "botanist_name": ["John Doe", "Jane Smith"]
    })

    resulting_df = extract_first_name_last_name(df)

    assert resulting_df["botanist_first_name"].tolist() == ["John", "Jane"]

    assert resulting_df["botanist_last_name"].tolist() == ["Doe", "Smith"]

    assert "botanist_name" not in resulting_df.columns
