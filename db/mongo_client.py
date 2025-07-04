import streamlit as st
from pymongo import MongoClient

@st.cache_resource
def get_mongo():
    uri = st.secrets["mongodb"]["MONGO_URI"]
    client = MongoClient(uri)
    return client["nps_app"]