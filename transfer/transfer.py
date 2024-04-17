"""This file is responsible for transfer old data from the sql server to an s3 bucket"""
from os import environ

from dotenv import load_dotenv
from pymssql import connect


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


if __name__ == "__main__":
    load_dotenv()
