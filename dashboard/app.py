"""This file contains script responsible for making a dashboard."""
from os import environ
import pandas as pd
import streamlit as st
import altair as alt
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

def db_data(conn,sql_query):
    """Loads data from redshift db."""
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
    recording_data =db_data(conn,"SELECT * FROM s_delta.recordings;")
    plant_data = db_data(conn,"SELECT * FROM s_delta.plant;")
    botanist_data = db_data(conn,"SELECT * FROM s_delta.botanist;")
    data_load_state.text('Loading data...done!')
    st.title('LNMH Plants Dashboard :potted_plant:')
    st.subheader(
        "Monitoring the health of  LNMH Plants")
    st.sidebar.header("LNMH Plant Dashboard")
    st.sidebar.subheader("Controls")

    plant_list = st.sidebar.multiselect("Plant ID",
                                        recording_data["plant_id"].unique(),
                                        recording_data["plant_id"].unique())
    
    relevant_plant_recordings = recording_data[recording_data["plant_id"].isin(plant_list)]
    relevant_plant_data = plant_data[plant_data["plant_id"].isin(plant_list)]

    plant_num = relevant_plant_data['plant_id'].count()
    botanist_num = botanist_data['botanist_id'].count()
    ten_minutes_ago = pd.Timestamp.now() - pd.Timedelta(hours=1,minutes=10)
    previous_day= pd.Timestamp.now() - pd.Timedelta(days=1,hours=1)

    average_plant_moisture_ten_mins_ago = relevant_plant_recordings[relevant_plant_recordings['recording_taken']>ten_minutes_ago]['soil_moisture'].mean().round(2)
    average_plant_temp_ten_mins_ago = relevant_plant_recordings[relevant_plant_recordings['recording_taken']>ten_minutes_ago]['temperature'].mean().round(2)
    plant_recordings_previous_day = relevant_plant_recordings[relevant_plant_recordings['recording_taken'].dt.date>previous_day.date()]
    botanist_data['num_plants'] = relevant_plant_recordings.groupby('botanist_id')['plant_id'].nunique().values

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Number of plants :herb:",
                  plant_num)
    with col2:
        st.metric("Number of botanists :female-farmer:",
                  botanist_num)
    
    with col3:
        st.metric("Average of soil moisture (<10 mins) :droplet:",average_plant_moisture_ten_mins_ago)
    
    with col4:
        st.metric("Average temperature (<10 mins) :thermometer:",average_plant_temp_ten_mins_ago)
    st.write(" ")
    left,middle,right = st.columns(3)
    choice = st.selectbox('Select a plant:',plant_list)
    
    with left:
        st.altair_chart(
        alt.Chart(plant_recordings_previous_day[plant_recordings_previous_day['plant_id']==choice],title=f"Temperature of plant {choice} today").mark_line().encode(
        x='recording_taken:T',
        y='temperature',
         color=alt.Color('plant_id:N', scale=alt.Scale(scheme='set2'))), use_container_width=True)
    with middle:
        st.altair_chart(
            alt.Chart(plant_recordings_previous_day[plant_recordings_previous_day['plant_id']==choice],title=f"Soil Moisture of plant {choice} today").mark_line().encode(
            x='recording_taken:T',
            y='soil_moisture',
            color=alt.Color('plant_id:N', scale=alt.Scale(scheme='set2'))), use_container_width=True)
    with right:
         st.altair_chart(
        alt.Chart(botanist_data,title="Number of plants per botanist").mark_arc().encode(
            theta="num_plants",
            color=alt.Color('first_name', scale=alt.Scale(scheme='set2'))), use_container_width=True)
