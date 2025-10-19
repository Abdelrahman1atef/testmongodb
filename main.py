# main.py
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.models.user_model import User
from database import init_db
from app.routes import user_routes

load_dotenv()
app = FastAPI()
app.include_router(user_routes.router)

@app.on_event("startup")
async def app_init():
    await init_db()
    print("✅ Database initialized successfully")

@app.get("/")
async def home():
    return {"message": "FastAPI + Beanie ODM connected!"}

