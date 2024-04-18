"""This file contains tests for the transfer function."""

import pandas as pd

from transfer import append_to_csv


def test_append_to_empty_csv(tmpdir):
    """
    Tests that `append_to_csv` correctly initialises an empty CSV with new data.
    """

    temp_csv_file_path = tmpdir.join("empty.csv")
    temp_csv_file_path.write('')
    test_dataset = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})

    append_to_csv(str(temp_csv_file_path), test_dataset)

    resulting_df = pd.read_csv(str(temp_csv_file_path))

    pd.testing.assert_frame_equal(test_dataset, resulting_df)


def test_append_to_existing_csv(tmpdir):
    """
    Tests that `append_to_csv` appends data to an existing CSV without header duplication.
    """

    temp_csv_file_path = tmpdir.join("existing.csv")
    initial_dataset = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    initial_dataset.to_csv(str(temp_csv_file_path), index=False)
    additional_dataset = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})

    append_to_csv(str(temp_csv_file_path), additional_dataset)

    expected_df = pd.concat([initial_dataset, additional_dataset], ignore_index=True)
    resulting_df = pd.read_csv(str(temp_csv_file_path))

    pd.testing.assert_frame_equal(expected_df, resulting_df)
