from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# การตั้งค่าเชื่อมต่อ MariaDB (ปรับให้ตรงกับเครื่องคุณ)
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "", # ใส่รหัสผ่านถ้ามี
    "database": "dorm_db"
}

# --- Pydantic Models (Data Validation) ---
class RepairRequest(BaseModel):
    room_number: str
    description: str

# --- API Endpoints (CRUD) ---

# 1. รับข้อมูลแจ้งซ่อม (Create)
@app.post("/repairs/")
def create_repair(repair: RepairRequest):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO repairs (room_number, description) VALUES (%s, %s)"
        cursor.execute(query, (repair.room_number, repair.description))
        conn.commit()
        return {"message": "แจ้งซ่อมสำเร็จ!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# 2. ดึงข้อมูลห้องพัก (Read)
@app.get("/rooms/{room_no}")
def get_room_info(room_no: str):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM rooms WHERE room_number = %s", (room_no,))
    result = cursor.fetchone()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="ไม่พบห้องนี้")
    return result