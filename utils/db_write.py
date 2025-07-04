# utils/db_write.py
from db.mongo_client import get_mongo
from datetime import datetime

def save_rating(user, effect, category_score, polarity_score, example_score):
    db = get_mongo()
    ratings = db["ratings"]
    doc = {
        "user": user,
        "effect": effect,
        "category_score": category_score,
        "polarity_score": polarity_score,
        "example_score": example_score,
        "timestamp": datetime.utcnow()
    }
    ratings.insert_one(doc)

def save_edit(user, effect, new_category, new_polarity, new_examples):
    db = get_mongo()
    edits = db["edits"]
    doc = {
        "user": user,
        "effect": effect,
        "new_category": new_category,
        "new_polarity": new_polarity,
        "new_examples": [e.strip() for e in new_examples.split(",")],
        "timestamp": datetime.utcnow(),
        "approved": False
    }
    edits.insert_one(doc)
