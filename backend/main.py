# ==============================
# 7. FastAPI Application
# ==============================
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session
import database
from database import get_db

import models
import crud

from pydantic import BaseModel
from typing import List
from datetime import datetime

import serial_reader

import io
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# ------------------------------
# Create FastAPI app
# ------------------------------
app = FastAPI(title="Telemetry Dashboard API")


# ------------------------------
# Enable CORS (cross-origin requests)
# ------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all frontends to access the API
    allow_credentials=True,
    allow_methods=["*"],  # Allow GET, POST, PUT, DELETE
    allow_headers=["*"],  # Allow any headers
)

# ------------------------------
# Serve static dashboard files
# ------------------------------
app.mount("/dashboard", StaticFiles(directory="dashboard"), name="dashboard")

# ------------------------------
# Start serial reader (Arduino/ESP32) - removed from backend
# ------------------------------
# serial_reader.start_serial()


# ==============================
# 8. Pydantic schema for optional POST endpoint
# ==============================
class TelemetryInput(BaseModel):
    temp: float  # temp: Optional[float] = None OR temp: float | None = None
    hum: float  # temp: Optional[float] = None OR temp: float | None = None
    mission_name: str = "Unnamed Mission"
    status: str = "Pending"
    timestamp: str


class MissionInput(BaseModel):
    mission_name: str


# ==============================
# 9. GET ENDPOINTS
# ==============================


@app.get("/telemetry/latest")
def get_latest(db: Session = Depends(get_db)):
    # Check latest saved entry in DB
    mission = db.query(models.Mission).order_by(models.Mission.timestamp.desc()).first()
    if mission:
        return {
            "TEMP": mission.temp,
            "HUM": mission.hum,
            "TIMESTAMP": mission.timestamp,
        }
    else:
        return {"TEMP": None, "HUM": None, "TIMESTAMP": None}


@app.get("/missions")
def list_missions(db: Session = Depends(database.get_db)):

    missions = crud.get_all_missions(db)
    return [
        {
            "id": m.id,
            "mission_name": m.mission_name,
            "temp": m.temp,
            "hum": m.hum,
            "timestamp": m.timestamp,
        }
        for m in missions
    ]


@app.get("/missions/{mission_name}")
def get_mission_data(mission_name: str, db: Session = Depends(get_db)):
    telemetry_data = crud.get_mission_by_name(db, mission_name)

    if not telemetry_data:
        raise HTTPException(status_code=404, detail="Mission not found")

    return [
        {
            "id": t.id,
            "mission_name": t.mission_name,
            "temp": t.temp,
            "hum": t.hum,
            "status": t.status,
            "timestamp": t.timestamp,
        }
        for t in telemetry_data
    ]


@app.get("/missions/{mission_name}/chart")
def get_mission_chart(mission_name: str, db: Session = Depends(database.get_db)):
    # Get all telemetry for this mission
    data = (
        db.query(models.Mission)
        .filter(models.Mission.mission_name == mission_name)
        .all()
    )
    if not data:
        raise HTTPException(status_code=404, detail="Mission not found")

    timestamps = [datetime.fromisoformat(d.timestamp) for d in data]
    temps = [d.temp for d in data]

    fig, ax = plt.subplots(figsize=(6, 4), facecolor="black")

    ax.plot(timestamps, temps, marker="o", linestyle="-", color="#00ffea", linewidth=2)

    ax.xaxis.set_major_locator(MaxNLocator(nbins=10))  # reduce number of ticks
    ax.set_xticklabels(
        [
            ts.strftime("%H:%M:%S")
            for ts in timestamps[:: max(1, len(timestamps) // 10)]
        ],
        color="whitesmoke",
        rotation=45,
    )

    # Axis labels and title
    ax.set_xlabel("Time", color="yellow")
    ax.set_ylabel("Temperature (°C)", color="yellow")
    ax.set_title(f"Temperature for {mission_name}", color="#ff69b4")

    # Set background color
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")

    # Grid and tick colors
    ax.grid(True, color="gray", linestyle="--", alpha=0.3)
    ax.tick_params(axis="y", colors="whitesmoke")

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", facecolor=fig.get_facecolor())
    plt.close()
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


# ==============================
#  POST ENDPOINT
# ==============================
@app.post("/telemetry")
def save_telemetry(data: TelemetryInput, db: Session = Depends(database.get_db)):
    mission = crud.save_reading(
        db,
        temp=data.temp,
        hum=data.hum,
        mission_name=data.mission_name,
        status=data.status,
        timestamp=data.timestamp,
    )
    return {"id": mission.id, "status": "saved"}
