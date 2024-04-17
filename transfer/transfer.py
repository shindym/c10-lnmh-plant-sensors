"""This file is responsible for transfer old data from the sql server to an s3 bucket"""
from os import environ

from boto3 import client
import botocore
from dotenv import load_dotenv
from pymssql import connect
import pandas as pd


LOCAL_FILE = "data/archived_data.csv"
BUCKET = "cretaceous-paleogene"
OBJECT_NAME = "archived_data.csv"


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
    Retrieves data older than 24 hours.
    """

    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM s_delta.recordings WHERE recording_taken < GETDATE()-1;")
        rows = cur.fetchall()
        cur.execute(
            "DELETE FROM s_delta.recordings WHERE recording_taken < GETDATE()-1;")
    conn.commit()

    return pd.DataFrame(rows)


def get_archive_file(aws_client, bucket_name, obj_name, download_path):
    try:
        aws_client.download_file(bucket_name, obj_name, download_path)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            with open(download_path, "w") as f:
                pass


def append_to_csv(csv, archive_data):
    try:
        pd.read_csv(csv)
    except pd.errors.EmptyDataError:
        archive_data.to_csv(csv, mode='w', index=False)
    else:
        archive_data.to_csv(csv, mode="a", index=False, header=False)


def add_new_csv_to_bucket(aws_client, filename, bucket, object_name):
    aws_client.upload_file(filename, bucket, object_name)


if __name__ == "__main__":
    load_dotenv()

    s3_client = client(
        "s3", aws_access_key_id=environ["ACCESS_KEY_ID"], aws_secret_access_key=environ["SECRET_ACCESS_KEY"])

    conn = get_db_connection(environ)
    old_data = retrieve_old_data(conn)

    get_archive_file(s3_client, BUCKET,
                     OBJECT_NAME, LOCAL_FILE)

    append_to_csv(LOCAL_FILE, old_data)

    add_new_csv_to_bucket(
        s3_client, LOCAL_FILE, BUCKET, OBJECT_NAME)
