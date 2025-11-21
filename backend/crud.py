# ==============================
# 4. CRUD Operations
# ==============================
from sqlalchemy.orm import Session
from datetime import datetime
import models

# ------------------------------
# Function: save_reading
# ------------------------------
def save_reading(db: Session, temp: float, hum: float, mission_name: str = None, status: str = "Pending", timestamp: str = None):
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    if mission_name is None:
        mission_name = "Unnamed Mission"

    mission = models.Mission(
        mission_name=mission_name,
        status=status,
        temp=temp,
        hum=hum,
        timestamp=timestamp
    )
    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission



# ------------------------------
# Function: get_all_missions
# ------------------------------
def get_all_missions(db: Session):
    """
    Retrieve all saved telemetry missions from the database.

    Parameters:
        db (Session): The active SQLAlchemy database session.

    Returns:
        list[models.Mission]: A list of all Mission records in the database.
    """
    # Perform SELECT * FROM missions
    return db.query(models.Mission).all()

# ------------------------------
# Function: get_mission_by_id (optional)
# ------------------------------
def get_mission_by_id(db: Session, mission_id: int):
    """
    Retrieve a single mission record by its ID.

    Parameters:
        db (Session): The active SQLAlchemy database session.
        mission_id (int): ID of the mission to retrieve.

    Returns:
        models.Mission or None: The mission record if found, else None.
    """
    return db.query(models.Mission).filter(models.Mission.id == mission_id).first()

# ------------------------------
# Function: delete_mission (optional)
# ------------------------------
def delete_mission(db: Session, mission_id: int):
    """
    Delete a mission record by its ID.

    Parameters:
        db (Session): The active SQLAlchemy database session.
        mission_id (int): ID of the mission to delete.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if mission:
        db.delete(mission)
        db.commit()
        return True
    return False
