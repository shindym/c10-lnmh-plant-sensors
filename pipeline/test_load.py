"""This file contains tests for the load function."""

import pandas as pd

from load import convert_to_list


def test_valid_csv_returns_list_of_tuples(tmpdir: str):
    """
    Tests that `convert_to_list` reads a valid CSV file and correctly converts to a list of tuples.
    """

    # Creating temporary CSV file with data
    temp_csv_file_path = tmpdir.join("test.csv")
    data = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    data.to_csv(temp_csv_file_path, index=False)

    result = convert_to_list(str(temp_csv_file_path))

    assert result == [(1, 3), (2, 4)]


def test_empty_csv_file_results_in_none(tmpdir):
    """
    Tests that `convert_to_list` returns None for an empty CSV file.
    """

    # Creating temporary empty CSV file with data
    temp_csv_file_path = tmpdir.join("empty.csv")
    pd.DataFrame().to_csv(temp_csv_file_path, index=False)

    result = convert_to_list(str(temp_csv_file_path))

    assert result is None


def test_non_existent_file_results_in_none():
    """
    Tests that `convert_to_list` returns None when the file does not exist.
    """

    result = convert_to_list("non-existent.csv")

    assert result is None
