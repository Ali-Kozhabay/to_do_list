from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from app.routes.tasks import router
from app.auth.auth_router import auth
import asyncio
from app.database import engine
app = FastAPI(
    title="Todo List API",
    description="A simple FastAPI application for managing to-do tasks with PostgreSQL",
    version="0.1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

conn=engine.connect()

# Create all tables in the database if they do not exist
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Run the create_tables function on startup
@app.on_event("startup")
async def on_startup():
    await create_tables()
app.include_router(router, prefix="/api/v1")
app.include_router(auth, prefix="/app/auth")

@app.get("/")
def root():
    return {
        "message": "Welcome to the Todo List API",
        "docs": "/docs",
        "version": "0.1.0"
    }
