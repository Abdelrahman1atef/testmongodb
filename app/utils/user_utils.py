# app/utils/bson_utils.py
from typing import Optional
from bson import ObjectId
from datetime import datetime

def obj_to_json(doc: Optional[dict]) -> Optional[dict]:
    """Convert Mongo document to JSON-serializable dict (ObjectId -> str)."""
    if not doc:
        return None
    doc = dict(doc)  # copy
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    # convert datetimes if needed (Motor returns datetime already serializable by FastAPI)
    return doc
