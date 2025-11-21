# ==============================
# 6. FastAPI Application
# ==============================
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
import database, crud, serial_reader, json

# ------------------------------
# Create FastAPI app
# ------------------------------
app = FastAPI(title="Telemetry Dashboard API")

# ------------------------------
# Enable CORS (cross-origin requests)
# ------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all frontends to access the API
    allow_credentials=True,
    allow_methods=["*"],      # Allow GET, POST, PUT, DELETE
    allow_headers=["*"],      # Allow any headers
)

# ------------------------------
# Serve static dashboard files
# ------------------------------
# Optional: serve frontend dashboard located in ../dashboard
app.mount("/dashboard", StaticFiles(directory="../dashboard"), name="dashboard")

# ------------------------------
# Start serial reader (Arduino/ESP32)
# ------------------------------
# Starts a background thread that continuously reads telemetry
serial_reader.start_serial()

# ==============================
# 7. Pydantic schema for optional POST endpoint
# ==============================
class TelemetryInput(BaseModel):
    temp: float
    hum: float
    mission_name: str = "Unnamed Mission"
    status: str = "Pending"
    timestamp: str

# ==============================
# 8. GET ENDPOINTS
# ==============================

@app.get("/telemetry/latest")
def get_latest():
    """
    Return the most recent telemetry reading from the Arduino.
    """
    try:
        return json.loads(serial_reader.latest_reading)
    except:
        # Return default values if no valid data is available
        return {"TEMP": None, "HUM": None}

@app.get("/missions")
def list_missions(db: Session = Depends(database.get_db)):
    """
    Return all saved telemetry readings from the database.
    """
    missions = crud.get_all_missions(db)
    # Convert SQLAlchemy objects to JSON-friendly dicts
    return [
        {"id": m.id, "temp": m.temp, "hum": m.hum, "timestamp": m.timestamp}
        for m in missions
    ]

# ==============================
#  OPTIONAL POST ENDPOINT
# ==============================
@app.post("/telemetry")
def save_telemetry(data: TelemetryInput, db: Session = Depends(database.get_db)):
    mission = crud.save_reading(
        db,
        temp=data.temp,
        hum=data.hum,
        mission_name=data.mission_name,
        status=data.status,
        timestamp=data.timestamp
    )
    return {"id": mission.id, "status": "saved"}