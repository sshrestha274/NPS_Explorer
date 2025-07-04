import streamlit as st
from auth.firebase_config import load_firebase
from db.mongo_client import get_mongo

st.set_page_config(page_title="Test Connections")

st.title("🔧 Diagnostic: Firebase + MongoDB")

# ---- Firebase Auth Check ---- #
st.subheader("Firebase Authentication")

try:
    auth = load_firebase()
    st.success("✅ Firebase auth loaded successfully.")
except Exception as e:
    st.error("❌ Failed to load Firebase auth.")
    st.exception(e)

# ---- MongoDB Check ---- #
st.subheader("MongoDB Connection")

try:
    db = get_mongo()
    st.success("✅ MongoDB connected.")
    
    # List collections for visual check
    st.write("Collections in DB:")
    st.code(db.list_collection_names())

    # Optionally check user role if logged in
    if "user_email" in st.session_state:
        user = db["users"].find_one({"email": st.session_state["user_email"]})
        if user:
            st.success(f"Logged in as {user['email']} with role: {user.get('role', 'N/A')}")
        else:
            st.warning("Logged-in user not found in MongoDB 'users' collection.")
    else:
        st.info("You are not logged in. Log in to verify user-level access.")

except Exception as e:
    st.error("❌ MongoDB connection failed.")
    st.exception(e)
