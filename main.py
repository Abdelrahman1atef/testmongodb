# main.py
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv
from app.models.user_model import User
from app.database.database import init_db
from app.routes import user_routes, auth_routes

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("✅ Database initialized successfully")
    # Startup events (executed before 'yield')
    print("Application startup initiated.")
    # Example: Initialize a database connection pool
    # app.state.db_pool = await create_db_pool() 
    yield
    # Shutdown events (executed after 'yield')
    print("Application shutdown initiated.")
    # Example: Close the database connection pool
    # await app.state.db_pool.close()
app = FastAPI(lifespan=lifespan)
# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include routers
app.include_router(auth_routes.router)
app.include_router(user_routes.router)

@app.get("/")
async def home():
    return {
        "message": "FastAPI MongoDB Auth API",
        "docs": "/docs",
        "redoc": "/redoc"
    }
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

