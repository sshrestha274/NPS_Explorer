import streamlit as st
from db.mongo_client import get_mongo

def admin_panel():
    st.title("🛠️ Admin Panel: User Role Management")

    db = get_mongo()
    users_collection = db["users"]

    users = list(users_collection.find({}, {"_id": 0}))
    if not users:
        st.info("No users found.")
        return

    user_emails = [u["email"] for u in users]

    selected_email = st.selectbox("Select user to edit role", user_emails)

    selected_user = next((u for u in users if u["email"] == selected_email), None)
    if selected_user is None:
        st.error("Selected user not found.")
        return

    current_role = selected_user.get("role", "rater")
    st.write(f"Current role: **{current_role}**")

    new_role = st.selectbox("Assign new role", ["public", "rater", "editor", "admin"], index=["public", "rater", "editor", "admin"].index(current_role))

    if st.button("Update Role"):
        if new_role != current_role:
            users_collection.update_one({"email": selected_email}, {"$set": {"role": new_role}})
            st.success(f"Updated role of {selected_email} to {new_role}")
        else:
            st.info("Role unchanged.")
