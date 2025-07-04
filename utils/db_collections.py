from db.mongo_client import get_mongo

def get_collections():
    db = get_mongo()
    return {
        "ratings": db["ratings"],
        "edits": db["edits"],
        "users": db["users"],
        "effects": db["effects"]
    }
