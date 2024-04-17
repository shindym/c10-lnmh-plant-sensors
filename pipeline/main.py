from extract import get_all_plant_data,create_plant_csv
from transform import clean_data,add_botanist_id
from load import get_db_connection, convert_to_list, load_data
from dotenv import load_dotenv
from os import environ


def pipeline_process():
    load_dotenv()
    # extract
    plants = get_all_plant_data()
    create_plant_csv(plants)
    # transfer
    conn = get_db_connection(environ)
    clean_data("data/plant_data.csv")
    add_botanist_id("data/plant_data.csv", conn)
    # load 
    conn = get_db_connection(environ)
    data_to_upload = convert_to_list("data/clean_plant_data.csv")
    if data_to_upload:
        load_data(conn, data_to_upload)
        conn.close()


if __name__ == "__main__":
    pipeline_process()