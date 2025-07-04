
import pandas as pd
from db.mongo_client import get_mongo

def load_effects_data():
    db = get_mongo()
    effects_collection = db["effects"]
    effect_docs = list(effects_collection.find({}, {"_id": 0}))
    df = pd.DataFrame(effect_docs)

    return df