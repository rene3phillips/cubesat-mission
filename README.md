# CubeSat Telemetry Project

A small CubeSat telemetry system with Arduino sensor hardware, a Python FastAPI backend, and a live updating web dashboard.

## Folder Structure

```bash
cubesat-mission/
├── backend/ # FastAPI backend
│ └── main.py
├── hardware/ # Arduino code
│ └── sensor.ino
├── dashboard/ # Frontend HTML dashboard
│ └── index.html
└── README.md
```


## Requirements

- Python 3.10+  
- PlatformIO / Arduino IDE  
- Arduino with DHT22/AM2302 sensor  
- Python packages:

```bash
pip install fastapi uvicorn pyserial
```

## Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/rene3phillips/cubesat-mission.git
cd cubesat-mission
```

2. Set up Arduino
- Open hardware/sensor.ino in PlatformIO or Arduino IDE.
- Connect your sensor:
    - VCC → 5V
    - GND → GND
    - Data → Digital Pin 2
- Upload the code to your Arduino.
- Make sure Serial Monitor is closed when running FastAPI.

3. Set up backend
- Navigate to the backend folder:
```bash
cd backend
python -m venv venv           # create virtual environment
source venv/bin/activate      # on Mac/Linux
venv\Scripts\activate         # on Windows
pip install -r requirements.txt  
```
- Run the FastAPI server:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

4. Open the dashboard
- Open your browser and go to:
```bash
http://127.0.0.1:8000/dashboard/index.html
```
- The telemetry should update every 2 seconds automatically.

## Notes
- Only one program can access the Arduino serial port at a time. Make sure PlatformIO Serial Monitor is closed when running the FastAPI server.
- The dashboard fetches /telemetry/latest from the same server to avoid CORS issues.