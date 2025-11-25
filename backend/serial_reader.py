# ==============================
# 6. Serial Reader
# ==============================

import serial
import threading
import time
import json
from datetime import datetime

# Stores the latest telemetry reading as a JSON string
latest_reading = json.dumps({"TEMP": None, "HUM": None, "TIMESTAMP": None})

def start_serial(port='COM4', baud=9600):
    """
    Opens the serial port and starts a background thread to continuously read telemetry.
    """
    global latest_reading

    try:
        ser = serial.Serial(port, baud, timeout=2)
        print(f"{port} opened successfully")
    except serial.SerialException as e:
        print(f"Error opening {port}: {e}")
        return

    def _read():
        global latest_reading
        while True:
            try:
                line = ser.readline().decode().strip()
                if line:
                    # Parse Arduino JSON
                    try:
                        data = json.loads(line)
                        temp = data.get("TEMP")
                        hum = data.get("HUM")
                        # Add server-side timestamp (local time)
                        data["TIMESTAMP"] = datetime.now().isoformat()

                        # Save latest reading globally
                        latest_reading = json.dumps(data)

                        # === REMOVE DB SAVE HERE ===
                        # Do NOT save here; frontend will handle saving when a mission is active
                        # This prevents the "Unnamed Mission" entries
                        # if temp is not None and hum is not None:
                        #     db = SessionLocal()
                        #     try:
                        #         crud.save_reading(db, temp, hum)
                        #         print(f"Saved: TEMP={temp}, HUM={hum}")
                        #     finally:
                        #         db.close()

                    except Exception as e:
                        print(f"Failed to parse line: {line} -> {e}")

            except Exception as e:
                print(f"Serial read error: {e}")

            time.sleep(0.1)

    threading.Thread(target=_read, daemon=True).start()
