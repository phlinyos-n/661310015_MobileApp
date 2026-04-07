from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "", 
    "database": "dorm_db",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}

class RepairCreate(BaseModel):
    room_number: str
    description: str

# 1. ค้นหาผู้เช่า (ที่แสดงอยู่ในรูปปัจจุบันของคุณ)
@app.get("/rooms/{room_no}")
def get_room(room_no: str):
    try:
        conn = pymysql.connect(**db_config)
        with conn.cursor() as cursor:
            cursor.execute("SELECT room_number, tenant_name, job, image_url FROM rooms WHERE room_number = %s", (room_no,))
            room = cursor.fetchone()
        conn.close()
        if not room:
            raise HTTPException(status_code=404, detail="ไม่พบข้อมูลห้องนี้")
        return room
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. แจ้งซ่อม (เพิ่มกลับเข้าไปเพื่อให้ตาราง repairs ใช้งานได้)
@app.post("/repairs/")
def create_repair(repair: RepairCreate):
    try:
        conn = pymysql.connect(**db_config)
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO repairs (room_number, description) VALUES (%s, %s)", (repair.room_number, repair.description))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. ดึงข้อมูลใบแจ้งหนี้ (เพิ่มกลับเข้าไปตามโครงสร้างตาราง invoices)
@app.get("/invoices/{room_no}")
def get_invoice(room_no: str):
    try:
        conn = pymysql.connect(**db_config)
        with conn.cursor() as cursor:
            # ใช้ room_number เชื่อมโยงข้อมูล
            cursor.execute("SELECT * FROM invoices WHERE room_id = (SELECT id FROM rooms WHERE room_number = %s)", (room_no,))
            invoice = cursor.fetchone()
        conn.close()
        return invoice if invoice else {"detail": "ยังไม่มีใบแจ้งหนี้"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))