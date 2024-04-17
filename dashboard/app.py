"""This file contains script responsible for making a dashboard."""
from os import environ as environ
import pandas as pd
import streamlit as st
import altair as alt
from dotenv import load_dotenv
from pymssql import connect

if __name__ == "__main__":
    st.set_page_config(page_title='LNMH Plant Dashboard',
                       page_icon=":potted_plant:", layout="wide")
    st.title('LNMH Plants Dashboard :potted_plant:')
    st.subheader(
        "Monitoring the health of  LNMH Plants")
