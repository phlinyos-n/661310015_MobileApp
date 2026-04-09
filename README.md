# MobileApp ระบบจัดการหอพัก บันทึกเลขมิเตอร์น้ำ, สร้างใบแจ้งหนี้ PDF, แจ้งซ่อมในหอพัก
# 661310015 ณัฐชนน ผลินยศ
# วิธีการติดตั้งและรันโปรเจกต์
# 1. สภาพแวดล้อมที่รองรับ (Prerequisites)
เป็นการบอกผู้ใช้งานว่าต้องมีโปรแกรมอะไรในเครื่องบ้าง:

Python: เวอร์ชัน 3.8 ขึ้นไป

Database: MariaDB หรือ MySQL (ใช้งานผ่าน HeidiSQL หรือ XAMPP ได้)

# 2. ติดตั้งฐานข้อมูล (Database Setup)
บอกขั้นตอนการเตรียมข้อมูล:

เปิดโปรแกรมจัดการฐานข้อมูล (HeidiSQL)

สร้าง Database ใหม่ชื่อ dorm_db

ทำการ Import ไฟล์ database.sql ที่อยู่ใน Repository นี้เข้าไปเพื่อสร้างตารางและข้อมูลเริ่มต้น

# 3. ติดตั้ง Library ที่จำเป็น
บอกคำสั่งที่ใช้เตรียมความพร้อมของ Python:

เปิด Terminal หรือ Command Prompt ในโฟลเดอร์งานแล้วพิมพ์:
pip install -r requirements.txt
(คำสั่งนี้จะติดตั้ง FastAPI, Uvicorn, Flet และ PyMySQL ให้ครบในครั้งเดียว)

# 4. ตั้งค่าการเชื่อมต่อ (Configuration)
จุดสำคัญเพื่อให้โค้ดรันได้ในเครื่องอื่น:

Backend: ตรวจสอบในไฟล์ backend.py ตรงคำสั่ง pymysql.connect ว่า user และ password ตรงกับฐานข้อมูลในเครื่อง (เช่น root และไม่มีรหัสผ่าน)

Frontend: ตรวจสอบตัวแปร API_URL ให้เป็น "http://localhost:8000" หากรันในเครื่องเดียวกัน

# 5. วิธีการติดตั้งและรันโปรเจกต์ (Step-by-Step)
สรุปการรันงานให้เห็นภาพชัดเจน:

Step 1: รัน Backend ด้วยคำสั่ง python -m uvicorn backend:app --reload

Step 2: เข้าไปที่ http://127.0.0.1:8000/docs เพื่อเช็คความเรียบร้อย (ต้องขึ้น Code 200)

Step 3: รันหน้าแอปด้วยคำสั่ง flet run frontend.py เพื่อใช้งานจริง

#https://drive.google.com/file/d/1SUjTfiV2HT17kHRpQi-5h7fT2obAl0J2/view?usp=sharing
