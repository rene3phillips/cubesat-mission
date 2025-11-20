from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import database, crud, serial_reader, json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve dashboard (optional)
app.mount("/dashboard", StaticFiles(directory="../dashboard"), name="dashboard")

# Start reading from Arduino
serial_reader.start_serial()

# Get latest telemetry
@app.get("/telemetry/latest")
def get_latest():
    try:
        return json.loads(serial_reader.latest_reading)
    except:
        return {"TEMP": None, "HUM": None}

# Get all saved missions
@app.get("/missions")
def list_missions(db: Session = Depends(database.get_db)):
    missions = crud.get_all_missions(db)
    return [
        {"id": m.id, "temp": m.temp, "hum": m.hum, "timestamp": m.timestamp}
        for m in missions
    ]
