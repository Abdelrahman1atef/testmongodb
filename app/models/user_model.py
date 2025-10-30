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
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"
        allow_index_dropping = True
        indexes = [
            [("email", pymongo.ASCENDING)],  # Unique email index
            [("created_at", pymongo.ASCENDING)]
        ]
    
    class Configg:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "strongpassword123"
            }
        }
        