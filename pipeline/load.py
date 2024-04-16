"""This file is responsible for loading the clean data into the database"""

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
    
    conn = get_db_connection(environ)
