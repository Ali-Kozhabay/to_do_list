import os

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.config import get_settings


settings=get_settings()




# Convert standard PostgreSQL URL to async format
async_db_url = settings.database_url
# Create async engine
engine = create_async_engine(
    async_db_url,
  # Log SQL queries
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(engine)


# Create declarative base class for SQLAlchemy models
Base = declarative_base()

# Dependency to get DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function that yields db sessions
    """
    async with AsyncSessionLocal() as session:
            yield session
