"""This file is responsible for cleaning and preparing plant data"""

from os import path, environ

import pandas as pd
from dotenv import load_dotenv
from pymssql import connect

from alert import Alerter

botanist_cache = {}


def get_db_connection(config):
    """
    Returns a connection to a database.
    """

    return connect(
        server=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"],
        port=config["DB_PORT"],
        as_dict=True
    )


def extract_first_name_last_name(df: pd.DataFrame) -> pd.DataFrame:
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
    Also converts data types of columns to appropriate types.
    """

    if not path.isfile(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    df = pd.read_csv(filename)

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


def find_botanist_id(x, conn):
    """
    Checks cache to see if email has been seen before (and therefore the id too),
    if not will access the database and find the id corresponding with this email.
    """

    if x not in botanist_cache:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT botanist_id FROM s_delta.botanist WHERE s_delta.botanist.email = %s", x)
            row = cur.fetchone()
        botanist_cache[x] = int(row["botanist_id"])
    return botanist_cache[x]


def add_botanist_id(filename: str, conn):
    """
    Shapes the data in a new csv for ease of use in the load script.
    Also adds a botanist id.
    """

    df = pd.read_csv(filename)
    df["botanist_id"] = df["botanist_email"].apply(
        find_botanist_id, args=(conn,))
    df = df.drop(
        columns=["botanist_first_name", "botanist_last_name", "botanist_email", "botanist_phone", "plant_common_name",
                 "plant_scientific_name", "origin_area", "origin_latitude", "origin_longitude"])

    # Rearranging columns to make it easier in the load script
    recording_taken = df.pop("recording_taken")
    last_watered = df.pop("last_watered")
    plant_id = df.pop("plant_id")
    df.insert(0, "recording_taken", recording_taken)
    df.insert(1, "last_watered", last_watered)
    df.insert(4, "plant_id", plant_id)

    df.to_csv(f"{environ['storage_folder']}/clean_plant_data.csv", index=False)


def send_alerts(conn):
    """
    Determines if the current values of soil_moisture and temperature are alert-worthy,
    sends an alert if so.
    """

    alerter = Alerter(environ)
    emails = alerter.get_email_addresses_from_names(
        ["setinder.manic", "ariba.syeda", "lucie.gamby"])

    current = pd.read_csv(f"{environ['storage_folder']}/clean_plant_data.csv")

    plants = current["plant_id"].to_list()

    # Checking for temperature fluctuations
    i = 0
    for plant in plants:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT TOP 3 * FROM s_delta.recordings WHERE plant_id = %s ORDER BY recording_taken DESC;", plant)
            row = cur.fetchall()
            this_plant = current[current["plant_id"] == plant].to_dict()

            # Checks for temperature fluctuations (accounts for erroneous spikes)
            if abs(row[0]["temperature"] - row[1]["temperature"]) > 5 and abs(this_plant["temperature"][i] - row[0]["temperature"]) < 3 and abs(row[1]["temperature"] - row[2]["temperature"]) < 3:
                # Send alert, temp fluctuation detected
                alerter.send_plain_email(
                    emails, "Plant {plant_num} Alert", f"Temperature fluctuation detected for plant {plant}!")
            i += 1

    # Checking average soil moisture
    if current["soil_moisture"].mean() < 15:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT soil_moisture FROM s_delta.recordings;", plant)
            rows = pd.DataFrame(cur.fetchall())
            recent_rows = rows.tail(len(plants))
            average = recent_rows["soil_moisture"].mean()
            if average > 15:
                # Send alert, average moisture too low
                alerter.send_plain_email(
                    emails, "Soil Moisture Alert", f"Average soil moisture is below 15 - plants need watering!")


if __name__ == "__main__":
    load_dotenv()

    conn = get_db_connection(environ)

    clean_data(f"{environ['storage_folder']}/plant_data.csv")
    add_botanist_id(f"{environ['storage_folder']}/plant_data.csv", conn)
    send_alerts(conn)
