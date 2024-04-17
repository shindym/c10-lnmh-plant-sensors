"""This file is responsible for cleaning and preparing plant data"""
from os import path

import pandas as pd


def extract_first_name_last_name(df: pd.DataFrame):
    """
    Splits up "botanist_name" into first_name and last_name.
    Drops "botanist_name" column when done.
    """

    df[['botanist_first_name', 'botanist_last_name']
       ] = df['botanist_name'].str.split(' ', expand=True)
    first_name = df.pop("botanist_first_name")
    last_name = df.pop("botanist_last_name")
    df.insert(1, "botanist_first_name", first_name)
    df.insert(2, "botanist_last_name", last_name)
    df = df.drop('botanist_name', axis=1)
    return df


def clean_data(filename: str):
    """
    Checks that soil moisture is between 0 and 100,
    and temperature is between 0 and 50.
    """

    if path.isfile(f"{filename}"):
        df = pd.read_csv(f"{filename}")
        df = extract_first_name_last_name(df)
        df = df[df['soil_moisture'] > 0]
        df = df[df['soil_moisture'] < 100]
        df = df[df['temperature'] > 0]
        df = df[df['temperature'] < 50]

        df["botanist_first_name"] = df["botanist_first_name"].astype("string")
        df["botanist_last_name"] = df["botanist_last_name"].astype("string")
        df["botanist_email"] = df["botanist_email"].astype("string")
        df["botanist_phone"] = df["botanist_phone"].astype("string")
        df["last_watered"] = pd.to_datetime(df["last_watered"])
        df["plant_common_name"] = df["plant_common_name"].astype("string")
        df["plant_scientific_name"] = df["plant_scientific_name"].astype(
            "string")
        df["origin_area"] = df["origin_area"].astype("string")
        df["recording_taken"] = df["recording_taken"].astype("datetime64[ns]")

        df.to_csv(filename, index=False)


if __name__ == "__main__":
    clean_data("data/plant_data.csv")
