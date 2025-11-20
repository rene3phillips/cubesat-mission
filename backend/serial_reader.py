import serial, threading, time, json
from database import SessionLocal
import crud

latest_reading = "No data yet"

def start_serial(port='COM4', baud=9600):
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
                    latest_reading = line
                    try:
                        data = json.loads(line)
                        temp = data.get("TEMP")
                        hum = data.get("HUM")
                        if temp is not None and hum is not None:
                            db = SessionLocal()
                            try:
                                crud.save_reading(db, temp, hum)
                                print(f"Saved: TEMP={temp}, HUM={hum}")
                            finally:
                                db.close()
                    except Exception as e:
                        print(f"Failed to parse/save line: {line} -> {e}")
            except Exception as e:
                print(f"Serial read error: {e}")
            time.sleep(0.1)

    threading.Thread(target=_read, daemon=True).start()
