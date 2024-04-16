"""This file is responsible for cleaning and preparing plant data"""
from os import path

import pandas as pd

def extract_first_name_last_name(df: pd.DataFrame):
    df[['botanist_first_name', 'botanist_last_name']]= df['botanist_name'].str.split(' ', expand=True)
    first_name = df.pop("botanist_first_name")
    last_name = df.pop("botanist_last_name")
    df.insert(1, "botanist_first_name", first_name)
    df.insert(2, "botanist_last_name", last_name)
    df = df.drop('botanist_name', axis=1)
    return df

def clean_data(filename: str):
    if path.isfile(f"{filename}"):
        df = pd.read_csv(f"{filename}")
        df = extract_first_name_last_name(df)
        df = df[df['soil_moisture'] > 0]
        df = df[df['soil_moisture'] < 100]
        df = df[df['temperature'] > 0]
        df = df[df['temperature'] < 50]
        df.to_csv(filename, index=False)

if __name__ == "__main__":
    clean_data("data/plant_data.csv")
