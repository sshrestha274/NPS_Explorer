import streamlit as st
import pyrebase

def load_firebase():
    config = st.secrets["firebase"]
    firebase = pyrebase.initialize_app(config)
    return firebase.auth()