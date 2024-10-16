import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from domain.models import Base
from sqlalchemy import text

# Set up the database URL from environment variable or default to a local PostgreSQL instance
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:password@db:5432/postgres")

# Create an asynchronous engine for connecting to the database
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create a session factory bound to the asynchronous engine
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    """
    Initialize the database by creating all tables and enabling the necessary PostgreSQL extensions.

    This function runs at the start of the application to:
    1. Ensure all tables defined in the ORM models (Base) are created in the database.
    2. Ensure the 'vector' extension for PostgreSQL is enabled, which is required for vector operations.

    Args:
        None

    Returns:
        None: This function performs database setup asynchronously and does not return any value.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Create tables based on models
        
        # Enable the 'vector' extension, if possible
        try:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        except Exception as e:
            print(f"Error enabling vector extension: {e}")  # Log error if extension fails
