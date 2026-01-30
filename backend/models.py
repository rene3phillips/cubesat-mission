# ==============================
# 1. Define Database Models
# ==============================
from sqlalchemy import Column, Integer, Float, String
from database import Base  # Import the Base class from database.py


class Mission(Base):

    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    mission_name = Column(String, nullable=False, default="Unnamed Mission")
    status = Column(String, nullable=False, default="Pending")
    temp = Column(Float, nullable=False)
    hum = Column(Float, nullable=False)
    timestamp = Column(String, nullable=False)
