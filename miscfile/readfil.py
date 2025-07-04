from pymongo import MongoClient
import streamlit as st

@st.cache_resource
def get_mongo():
    uri = st.secrets["MONGO_URI"]
    client = MongoClient(uri)
    return client["nps_app"]

db = get_mongo()
effects = db["effects"]

import pandas as pd

df = pd.read_csv("nps_effects_lexicon_extended_examples.csv")
records = df.to_dict("records")

# Convert semicolon-separated strings to list
for r in records:
    r["example_phrases"] = [x.strip() for x in r["example_phrases"].split(";")]

effects.insert_many(records)