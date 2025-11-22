# ==============================
# 5. Define Database Models
# ==============================
from sqlalchemy import Column, Integer, Float, String
from database import Base  # Import the Base class from database.py

class Mission(Base): # change to telemetry !!!
    """
    Mission model represents a telemetry reading in the database.

    Each instance corresponds to one row in the 'missions' table.
    """

    # Name of the table in PostgreSQL
    __tablename__ = "missions" # change to telemetry !!!

    # ------------------------------
    # Columns
    # ------------------------------

    # Primary key for the table, auto-incrementing integer
    # Indexed for faster queries
    id = Column(Integer, primary_key=True, index=True)

    mission_name = Column(String, nullable=False, default="Unnamed Mission")

    status = Column(String, nullable=False, default="Pending")

    # Temperature value from the sensor (cannot be null)
    temp = Column(Float, nullable=False)

    # Humidity value from the sensor (cannot be null)
    hum = Column(Float, nullable=False)

    # Timestamp of the reading in ISO format (cannot be null)
    timestamp = Column(String, nullable=False)
