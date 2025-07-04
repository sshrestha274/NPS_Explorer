import streamlit as st
from auth.firebase_config import load_firebase
from db.mongo_client import get_mongo

def get_user_role(email, default_role="rater"):
    db = get_mongo()
    users = db["users"]
    user = users.find_one({"email": email})
    if user and "role" in user:
        return user["role"]
    else:
        # Optionally: create new user if not exists
        users.insert_one({"email": email, "role": default_role})
        return default_role

def login_ui():
    auth = load_firebase()

    if "user_email" in st.session_state:
        st.sidebar.write(f"✅ Logged in as: `{st.session_state['user_email']}` ({st.session_state.get('role', 'unknown')})")
        if st.sidebar.button("Logout"):
            for key in ["user_email", "auth_token", "role"]:
                st.session_state.pop(key, None)
            st.rerun()
    else:
        mode = st.sidebar.radio("Choose action", ["Login", "Register"])
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button(mode):
            if not email or not password:
                st.error("Please enter both email and password.")
                return
            if mode == "Login":
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    st.session_state["user_email"] = email
                    st.session_state["auth_token"] = user["idToken"]
                    st.session_state["role"] = get_user_role(email)
                    st.success(f"Welcome back, {email}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {e}")
            else:  # Register
                try:
                    user = auth.create_user_with_email_and_password(email, password)
                    st.success(f"Account created for {email}. Please log in.")
                    # Add default role to DB
                    get_user_role(email, default_role="rater")
                except Exception as e:
                    st.error(f"Registration failed: {e}")
