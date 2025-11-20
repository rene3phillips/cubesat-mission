from sqlalchemy import Column, Integer, Float, String
from database import Base  # Use the Base from database.py

class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    temp = Column(Float, nullable=False)
    hum = Column(Float, nullable=False)
    timestamp = Column(String, nullable=False)
