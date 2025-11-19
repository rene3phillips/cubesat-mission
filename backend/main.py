from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import serial
import threading
import time

# 1️⃣ Create the FastAPI app 
app = FastAPI()

# 2️⃣ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3️⃣ Serve the dashboard folder
app.mount("/dashboard", StaticFiles(directory="../dashboard"), name="dashboard")

# 4️⃣ Initialize latest reading
latest_reading = "No data yet"

# 5️⃣ Open serial port
try:
    ser = serial.Serial('COM4', 9600, timeout=2)
    print("COM4 is free and opened successfully.")
except serial.SerialException as e:
    print(f"Error opening COM4: {e}")
    ser = None

# 6️⃣ Background thread to read Arduino
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

# 7️⃣ FastAPI endpoints
@app.get("/telemetry/latest")
def get_telemetry():
    return {"telemetry": latest_reading}

@app.get("/")
def home():
    return {"message": "CubeSat Telemetry API"}
