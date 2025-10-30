import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.models.user_model import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    MONGODB_URL = os.getenv("MONGODB_URL")
    DATABASE_NAME = os.getenv("SAMPLE_MFLIX_DATABASE_NAME")

    if not MONGODB_URL or not DATABASE_NAME:
        logger.error("MONGODB_URL or SAMPLE_MFLIX_DATABASE_NAME not set in environment")
        raise ValueError("Missing environment variables for MongoDB connection")

    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]

    # Initialize Beanie with the document models
    await init_beanie(database= db, document_models=[User]) # type: ignore
    print("Connected to MongoDB and initialized Beanie")