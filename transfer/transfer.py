"""This file is responsible for transfer old data from the sql server to an s3 bucket"""
from os import environ

from dotenv import load_dotenv
from pymssql import connect
import pandas as pd


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


def retrieve_old_data(conn):
    """
    Retrieves data older than 24 hours
    """

    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM s_delta.recordings WHERE recording_taken < GETDATE()-1;")
        rows = cur.fetchall()

    return pd.DataFrame(rows)


if __name__ == "__main__":
    load_dotenv()

    conn = get_db_connection(environ)
    old_data = retrieve_old_data(conn)
    print(old_data.head())
