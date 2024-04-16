"""This file is responsible for cleaning and preparing plant data"""
from os import path

import pandas as pd

def clean_data(filename: str):
    if path.isfile(f"{filename}"):
        df = pd.read_csv(f"{filename}")
        df = df[df['soil_moisture'] > 0]
        df = df[df['soil_moisture'] < 100]
        df = df[df['temperature'] > 0]
        df = df[df['temperature'] < 50]
        df.to_csv(filename, index=False)

if __name__ == "__main__":
    clean_data("data/plant_data.csv")
