from sqlalchemy.orm import Session
import models
from datetime import datetime

def save_reading(db: Session, temp: float, hum: float):
    """Save a single reading to the database."""
    mission = models.Mission(
        temp=temp,
        hum=hum,
        timestamp=datetime.utcnow().isoformat()
    )
    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission

def get_all_missions(db: Session):
    """Return all saved missions."""
    return db.query(models.Mission).all()
