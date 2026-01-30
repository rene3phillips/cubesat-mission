# ==============================
# 5. CRUD Operations
# ==============================
from sqlalchemy.orm import Session
from datetime import datetime
import models


# ------------------------------
# Function: save reading
# ------------------------------
def save_reading(
    db: Session,
    temp: float,
    hum: float,
    mission_name: str = None,
    status: str = "Pending",
    timestamp: str = None,
):
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    if mission_name is None:
        mission_name = "Unnamed Mission"

    mission = models.Mission(
        mission_name=mission_name,
        status=status,
        temp=temp,
        hum=hum,
        timestamp=timestamp,
    )
    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission


# ------------------------------
# Function: get_all_missions
# ------------------------------
def get_all_missions(db: Session):

    return db.query(models.Mission).all()


# ------------------------------
# Function: get_mission_by_id (optional)
# ------------------------------
def get_mission_by_id(db: Session, mission_id: int):

    return db.query(models.Mission).filter(models.Mission.id == mission_id).first()


# ------------------------------
# Function: delete_mission (optional)
# ------------------------------
def delete_mission(db: Session, mission_id: int):

    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if mission:
        db.delete(mission)
        db.commit()
        return True
    return False


# ------------------------------
# Function: get_mission_by_name
# ------------------------------
def get_mission_by_name(db: Session, mission_name: str):

    return (
        db.query(models.Mission)
        .filter(models.Mission.mission_name == mission_name)
        .all()
    )
