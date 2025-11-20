from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import serial
import threading
import time
import json

# Create the FastAPI app 
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the dashboard folder
app.mount("/dashboard", StaticFiles(directory="../dashboard"), name="dashboard")

# Initialize latest reading
latest_reading = "No data yet"

# Open serial port
try:
    ser = serial.Serial('COM4', 9600, timeout=2)
    print("COM4 is free and opened successfully.")
except serial.SerialException as e:
    print(f"Error opening COM4: {e}")
    ser = None

# Background thread to read Arduino
def read_serial():
    global latest_reading
    while ser:
        try:
            line = ser.readline().decode().strip()
            if line:
                latest_reading = line
        except:
            pass
        time.sleep(0.1)

if ser:
    threading.Thread(target=read_serial, daemon=True).start()

# FastAPI endpoints
@app.get("/telemetry/latest")
def get_telemetry():
    global latest_reading
    try:
        data = json.loads(latest_reading)  # parse JSON string from Arduino
    except:
        data = {"TEMP": None, "HUM": None}  # fallback if Arduino output is invalid
    return data