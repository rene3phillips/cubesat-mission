# ==============================
# 2. Connect to PostgreSQL
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
# 3. Set up SessionLocal
# ==============================
SessionLocal = sessionmaker(
    autocommit=False,   
    autoflush=False,    
    bind=engine         
)

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==============================
# 4. Set up Base for Models
# ==============================
Base = declarative_base()
