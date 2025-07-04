# import streamlit as st
# import pandas as pd
# import json
# import streamlit as st
# from pymongo import MongoClient

# # ----- IMPORTS ----- #

# @st.cache_resource
# def get_mongo():
#     uri = st.secrets["MONGO_URI"]
#     client = MongoClient(uri)
#     return client["nps_app"]

# db = get_mongo()
# ratings = db["ratings"]
# effects = db["effects"]
# users = db["users"]

# # # Load data
# # @st.cache_data
# # def load_data():
# #     return pd.read_csv("nps_effects_lexicon_extended_examples.csv")

# effect_docs = list(effects.find())
# df = pd.DataFrame(effect_docs)

# # ----- PAGE SETUP ----- #
# st.set_page_config(page_title="NPS Effects Explorer", layout="wide")
# st.title("🧠 NPS Effects Explorer")

# # ----- LANDING DESCRIPTION ----- #
# st.markdown("""
# Welcome to the **NPS Effects Explorer**.

# This tool provides descriptions of **psychological** and **physiological** effects associated with novel psychoactive substances (NPS). The purpose is to support community reporting, harm reduction, and research efforts by documenting subjective experiences from diverse sources.

# - **Public viewers** can review the lexicon.
# - **Logged-in users** can participate in evaluation (agreement scores).
# - **Contributors** can suggest edits or additions to improve accuracy.
# """)

# # ----- USER TYPE ----- #
# user_type = st.sidebar.selectbox("User Access Level", ["Public", "Rating Access", "Edit Access"])

# # ----- SELECT A FEELING ----- #
# effect_list = df['effect'].unique().tolist()
# selected_effect = st.selectbox("Select an Effect to Explore", sorted(effect_list))

# # ----- DISPLAY EFFECT METADATA ----- #
# effect_row = df[df['effect'] == selected_effect].iloc[0]
# st.subheader(f"🔍 Effect: {selected_effect}")
# # st.markdown(f"**Synonym**: {effect_row['synonyms']}")
# st.markdown(f"**Category**: {effect_row['category']}")
# st.markdown(f"**Polarity**: {effect_row['polarity']}")
# st.markdown("**Example Phrases:**")
# for example in effect_row['example_phrases']:
#     st.markdown(f"- {example.strip()}")

# # ----- RATING ACCESS USERS ----- #
# if user_type == "Rating Access":
#     st.subheader("📊 Rate This Entry")
#     category_score = st.slider("How accurate is the category?", 0, 10, 5)
#     polarity_score = st.slider("How accurate is the polarity?", 0, 10, 5)
#     example_score = st.slider("Are the examples representative?", 0, 10, 5)
#     st.button("Submit Ratings")

# # ----- EDIT ACCESS USERS ----- #
# if user_type == "Edit Access":
#     st.subheader("✏️ Edit This Entry")
#     new_category = st.text_input("Edit Category", value=effect_row['category'])
#     new_polarity = st.text_input("Edit Polarity", value=effect_row['polarity'])
#     new_examples = st.text_area("Edit Examples (separated by semicolons)", value=effect_row['example_phrases'])
#     if st.button("Submit Edit"):
#         st.success("Edits submitted. Changes would be reviewed and saved in admin backend.")


import streamlit as st
import pandas as pd

from utils.data_loader import load_effects_data
from utils.db_collections import get_collections
from utils.db_write import save_rating, save_edit
from auth.admin_panel import admin_panel
from auth.login import login_ui
from auth.user_roles import get_user_role


# ----- PAGE SETUP ----- #
st.set_page_config(page_title="NPS Effects Explorer", layout="wide")
st.title("🧠 NPS Effects Explorer")

# ----- LANDING DESCRIPTION ----- #
st.markdown("""
Welcome to the **NPS Effects Explorer**.

This tool provides descriptions of **psychological** and **physiological** effects associated with novel psychoactive substances (NPS). The purpose is to support community reporting, harm reduction, and research efforts by documenting subjective experiences from diverse sources.

- **Public viewers** can review the lexicon.
- **Logged-in users** can participate in evaluation (agreement scores).
- **Contributors** can suggest edits or additions to improve accuracy.
""")

# # ----- USER TYPE ----- #
# user_type = st.sidebar.selectbox("User Access Level", ["Public", "Rating Access", "Edit Access"])

# Run login UI sidebar
login_ui()

if "user_email" in st.session_state:
    role = get_user_role(st.session_state["user_email"])
else:
    role = "Public"

st.sidebar.markdown(f"**Role:** {role}")

if role.lower() == "admin":
    admin_panel()
else:
    st.write(f"Welcome, {st.session_state.get('user_email', 'Guest')}! You do not have admin access.")

st.sidebar.markdown(f"**Role:** {role.capitalize()}")

# --- Admin panel for admins ---
if role == "admin":
    admin_panel()
else:
    # --- Load data ---
    
    df = load_effects_data()
    collections = get_collections()
    ratings_col = collections["ratings"]
    edits_col = collections["edits"]

    # --- Select effect ---
    effect_list = df['effect'].unique().tolist()
    selected_effect = st.selectbox("Select an Effect to Explore", sorted(effect_list))
    effect_row = df[df['effect'] == selected_effect].iloc[0]

    # --- Display effect metadata ---
    st.subheader(f"🔍 Effect: {selected_effect}")
    st.markdown(f"**Category**: {effect_row['category']}")
    st.markdown(f"**Polarity**: {effect_row['polarity']}")
    st.markdown("**Example Phrases:**")
    for example in effect_row['example_phrases']:
        st.markdown(f"- {example.strip()}")

    # --- Role-based UI ---
    if role == "rater":
        st.subheader("📊 Rate This Entry")
        category_score = st.slider("How accurate is the category?", 0, 10, 5)
        polarity_score = st.slider("How accurate is the polarity?", 0, 10, 5)
        example_score = st.slider("Are the examples representative?", 0, 10, 5)
        if st.button("Submit Ratings"):
            save_rating(st.session_state["user_email"], selected_effect, category_score, polarity_score, example_score)
            st.success("Ratings submitted.")

    if role in ["editor", "admin"]:
        st.subheader("✏️ Edit This Entry")
        new_category = st.text_input("Edit Category", value=effect_row['category'])
        new_polarity = st.text_input("Edit Polarity", value=effect_row['polarity'])
        new_examples = st.text_area("Edit Examples (comma-separated)", value=", ".join(effect_row['example_phrases']))
        if st.button("Submit Edit"):
            if st.button("Submit Edit"):
                save_edit(st.session_state["user_email"], selected_effect, new_category, new_polarity, new_examples)
                st.success("Edits submitted.")