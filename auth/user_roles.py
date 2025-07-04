from db.mongo_client import get_mongo

def get_user_role(email):
    users = get_mongo()["users"]
    doc = users.find_one({"email": email})
    return doc["role"] if doc else "Public"