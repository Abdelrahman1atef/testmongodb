# app/models/user.py
from beanie import Document
from pydantic import EmailStr, Field
from typing import Optional
from datetime import datetime, timezone
import pymongo


class User(Document):
    name: str
    email: EmailStr
    password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    class Settings:
        name = "users"
        allow_index_dropping = True
        indexes = [
        [("created_at", pymongo.ASCENDING)]  # ✅ or just 1 (int)
    ]
        