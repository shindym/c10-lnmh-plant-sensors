"""This file contains script responsible for making a dashboard."""

from os import environ

import pandas as pd
import streamlit as st
import altair as alt
from dotenv import load_dotenv
from pymssql import connect
from boto3 import client


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


def connect_to_s3(config):

    """
    Returns s3 client object.
    """

    s3 = client('s3', aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'])

    return s3
  

def download_data_from_s3(client_obj) -> None:
    """
    Downloads archived_data.csv from S3 bucket.
    """

    client_obj.download_file("cretaceous-paleogene",
                             "archived_data.csv", "archived_data.csv")


def db_data(conn, sql_query: str) -> pd.DataFrame:
    """
    Loads data from redshift db.
    """

    with conn.cursor() as cur:
        cur.execute(sql_query)
        data = cur.fetchall()

    return pd.DataFrame(data)


if __name__ == "__main__":
    st.set_page_config(page_title='LNMH Plant Dashboard',
                       page_icon=":potted_plant:", layout="wide")
    load_dotenv()

    conn = get_db_connection(environ)
    data_load_state = st.text('Loading data...')
    recording_data = db_data(conn, "SELECT * FROM s_delta.recordings;")
    plant_data = db_data(conn, "SELECT * FROM s_delta.plant;")
    botanist_data = db_data(conn, "SELECT * FROM s_delta.botanist;")
    s3_client = connect_to_s3(environ)
    archived_data = download_data_from_s3(s3_client)
    archived_data = pd.read_csv('archived_data.csv')
    data_load_state.text('Loading data...done!')

    st.title('LNMH Plants Dashboard :potted_plant:')
    st.subheader(
        "Monitoring the health of  LNMH Plants")
    st.sidebar.header("LNMH Plant Dashboard")
    st.sidebar.subheader("Controls")

    plant_list = st.sidebar.multiselect("Plant ID",
                                        recording_data["plant_id"].unique(),
                                        recording_data["plant_id"].unique())
    x_days = st.sidebar.selectbox('Number of days ago:', [0, 1, 2, 3, 4, 5])
    choice = st.sidebar.selectbox('Select a plant:', plant_list)
    x_days_ago = pd.Timestamp.now() - pd.Timedelta(days=x_days, hours=1)

    relevant_plant_recordings = recording_data[recording_data["plant_id"].isin(plant_list)]
    relevant_plant_data = plant_data[plant_data["plant_id"].isin(plant_list)]
    relevant_archived_data = archived_data[archived_data["plant_id"].isin(plant_list)]

    plant_num = relevant_plant_data['plant_id'].count()
    botanist_num = botanist_data['botanist_id'].count()
    ten_minutes_ago = pd.Timestamp.now() - pd.Timedelta(hours=1, minutes=10)
    previous_day = pd.Timestamp.now() - pd.Timedelta(days=1, hours=1)

    average_plant_moisture_ten_mins_ago = relevant_plant_recordings[relevant_plant_recordings['recording_taken'] > ten_minutes_ago][
            'soil_moisture'].mean().round(2)
    average_plant_temp_ten_mins_ago = relevant_plant_recordings[relevant_plant_recordings['recording_taken'] > ten_minutes_ago][
            'temperature'].mean().round(2)
    plant_recordings_previous_day = relevant_plant_recordings[
        relevant_plant_recordings['recording_taken'].dt.date > previous_day.date()]
    botanist_data['num_plants'] = relevant_plant_recordings.groupby('botanist_id')['plant_id'].nunique().values
    frames = [archived_data, relevant_plant_recordings]

    combined_recording_data = pd.concat(frames)
    combined_recording_data['last_watered'] = pd.to_datetime(combined_recording_data['last_watered'])
    num_plants_watered_x_days_ago = \
        combined_recording_data[combined_recording_data['last_watered'].dt.date == x_days_ago.date()][
            'last_watered'].nunique()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Number of plants :herb:",
                  plant_num)
    with col2:
        st.metric("Number of botanists :female-farmer:",
                  botanist_num)

    with col3:
        st.metric("Average of soil moisture (<10 mins) :droplet:", average_plant_moisture_ten_mins_ago)

    with col4:
        st.metric("Average temperature (<10 mins) :thermometer:", average_plant_temp_ten_mins_ago)

    with col5:
        st.metric(f"Number of times watered {x_days} days ago :clock1:", num_plants_watered_x_days_ago)

    st.write(" ")
    left, middle, right = st.columns(3)

    with left:
        st.altair_chart(
            alt.Chart(plant_recordings_previous_day[plant_recordings_previous_day['plant_id'] == choice],
                      title=f"Temperature of plant {choice} today").mark_line().encode(
                x='recording_taken:T',
                y='temperature',
                color=alt.Color('plant_id:N', scale=alt.Scale(scheme='set2'))), use_container_width=True)
    with middle:
        st.altair_chart(
            alt.Chart(plant_recordings_previous_day[plant_recordings_previous_day['plant_id'] == choice],
                      title=f"Soil Moisture of plant {choice} today").mark_line().encode(
                x='recording_taken:T',
                y='soil_moisture',
                color=alt.Color('plant_id:N', scale=alt.Scale(scheme='set2'))), use_container_width=True)
    with right:
        st.altair_chart(
            alt.Chart(botanist_data, title="Number of plants per botanist").mark_arc().encode(
                theta="num_plants",
                color=alt.Color('first_name', scale=alt.Scale(scheme='set2'))), use_container_width=True)
