# ==============================
# 1. Connect to PostgreSQL
# ==============================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine (handles connection pool to PostgreSQL)
engine = create_engine(DATABASE_URL)

# ==============================
# 2️. Set up SessionLocal
# ==============================
# SessionLocal is a factory that generates new Session objects
# Each session is a workspace for interacting with the database
SessionLocal = sessionmaker(
    autocommit=False,   # Manual commit required
    autoflush=False,    # Prevent auto-flush until commit or query
    bind=engine         # Bind the session to the PostgreSQL engine
)

# Dependency for FastAPI endpoints
def get_db():
    """
    Create a new database session for a request, yield it to the endpoint,
    and close it after the request ends.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==============================
# 3️. Set up Base for Models
# ==============================
# Base is the parent class for all ORM models
# SQLAlchemy uses Base.metadata to know all tables for creation
Base = declarative_base()
