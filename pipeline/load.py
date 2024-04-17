"""This file is responsible for loading the clean data into the database"""

from os import path, environ as ENV

from dotenv import load_dotenv
from pymssql import connect
import pandas as pd

INSERT_RECORDING_QUERY = """
INSERT INTO 
    s_delta.recordings (recording_taken, last_watered, soil_moisture, temperature, plant_id, botanist_id)
VALUES 
    (%s, %s, %s, %s, %s, %s);
"""


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


def convert_to_list(filename):
    """Converts a DataFrame to a list of tuples."""

    if path.isfile(f"{filename}"):
        df = pd.read_csv(filename)

        return df.to_records(index=False).tolist() if not df.empty else None


def load_data(conn, data):
    """
    Loads the data into the database.
    """

    with conn.cursor() as cur:

        cur.executemany(INSERT_RECORDING_QUERY, data)

    conn.commit()


if __name__ == "__main__":
    load_dotenv()

    conn = get_db_connection(ENV)

    data_to_upload = convert_to_list("data/clean_plant_data.csv")

    if data_to_upload:
        load_data(conn, data_to_upload)

    conn.close()
