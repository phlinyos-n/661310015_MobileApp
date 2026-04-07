import flet as ft
import requests
from fpdf import FPDF

# URL ของ Backend (ต้องรัน uvicorn ก่อน)
API_URL = "http://127.0.0.1:8000"

def main(page: ft.Page):
    page.title = "Dormitory Management System"
    page.theme_mode = "light"
    page.window_width = 450
    page.window_height = 800
    # แก้ไขการจัดวางให้ถูกต้องตามเวอร์ชันล่าสุด
    page.vertical_alignment = ft.MainAxisAlignment.CENTER 
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def nav(target):
        login_pg.visible = (target == "login")
        menu_pg.visible = (target == "menu")
        search_pg.visible = (target == "search")
        repair_pg.visible = (target == "repair")
        meter_pg.visible = (target == "meter")
        page.update()

    # --- หน้า Login ---
    user_in = ft.TextField(label="Username", width=300, border_radius=10)
    pass_in = ft.TextField(label="Password", password=True, width=300, border_radius=10)
    login_pg = ft.Column([
        ft.Text("ระบบจัดการหอพัก", size=30, weight="bold", color="blue700"),
        user_in, pass_in,
        ft.ElevatedButton("เข้าสู่ระบบ", on_click=lambda _: nav("menu"), width=300, height=50),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, visible=True)

    # --- หน้าเมนูหลัก ---
    menu_pg = ft.Column([
        ft.Text("เมนูหลัก", size=24, weight="bold"),
        ft.ElevatedButton("🔍 ตรวจข้อมูลผู้เช่า", on_click=lambda _: nav("search"), width=300, height=50),
        ft.ElevatedButton("🛠️ แจ้งซ่อมบำรุง", on_click=lambda _: nav("repair"), width=300, height=50),
        ft.ElevatedButton("💰 บันทึกมิเตอร์/ออกบิล", on_click=lambda _: nav("meter"), width=300, height=50),
        ft.TextButton("ออกจากระบบ", on_click=lambda _: nav("login")),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, visible=False)

    # --- หน้าตรวจสอบข้อมูล (ดึงจาก MariaDB ผ่าน API) ---
    room_search = ft.TextField(label="เลขห้อง (เช่น 101)", width=300)
    res_display = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def do_search(e):
        res_display.controls.clear()
        try:
            r = requests.get(f"{API_URL}/rooms/{room_search.value}")
            if r.status_code == 200:
                data = r.json()
                res_display.controls.append(ft.Card(content=ft.Container(padding=20, content=ft.Column([
                    ft.Text(f"ห้อง: {data['room_number']}", size=20, weight="bold"),
                    ft.Text(f"ผู้เช่า: {data['tenant_name'] or 'ไม่มีข้อมูล'}")
                ]))))
            else: res_display.controls.append(ft.Text("❌ ไม่พบข้อมูล", color="red"))
        except: res_display.controls.append(ft.Text("⚠️ เชื่อมต่อ API ไม่ได้", color="orange"))
        page.update()

    search_pg = ft.Column([
        ft.Text("ค้นหาข้อมูลผู้เช่า", size=22),
        room_search, ft.ElevatedButton("ค้นหา", on_click=do_search),
        res_display, ft.TextButton("กลับ", on_click=lambda _: nav("menu"))
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, visible=False)

    # --- หน้าแจ้งซ่อม (ส่งข้อมูลเข้า DB) ---
    rep_room = ft.TextField(label="เลขห้อง", width=300)
    rep_desc = ft.TextField(label="อาการที่เสีย", multiline=True, width=300)

    def send_repair(e):
        try:
            payload = {"room_number": rep_room.value, "description": rep_desc.value}
            res = requests.post(f"{API_URL}/repairs/", json=payload)
            if res.status_code == 200:
                page.snack_bar = ft.SnackBar(ft.Text("✅ บันทึกข้อมูลแจ้งซ่อมแล้ว"))
                rep_room.value = ""; rep_desc.value = ""
            page.snack_bar.open = True
        except: pass
        page.update()

    repair_pg = ft.Column([
        ft.Text("รายการแจ้งซ่อม", size=22),
        rep_room, rep_desc,
        ft.ElevatedButton("ยืนยันการแจ้งซ่อม", on_click=send_repair, width=300),
        ft.TextButton("กลับ", on_click=lambda _: nav("menu"))
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, visible=False)

    # --- หน้าบันทึกมิเตอร์ & แยกปุ่มพิมพ์ PDF ---
    m_room = ft.TextField(label="เลขห้อง", width=300)
    m_water = ft.TextField(label="หน่วยน้ำ", width=300)
    m_elec = ft.TextField(label="หน่วยไฟ", width=300)
    calc_res = ft.Column()
    
    bill_info = {}

    def calculate(e):
        w = float(m_water.value or 0) * 15
        el = float(m_elec.value or 0) * 4.5
        total = 4500 + w + el
        bill_info.update({"room": m_room.value, "total": total})
        calc_res.controls.clear()
        calc_res.controls.append(ft.Text(f"ยอดรวม: {total:,.2f} บาท", size=20, color="blue", weight="bold"))
        btn_pdf.disabled = False
        page.update()

    def print_pdf(e):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Invoice Room: {bill_info['room']}", ln=True)
        pdf.cell(200, 10, txt=f"Total Amount: {bill_info['total']:.2f} THB", ln=True)
        pdf.output(f"Bill_{bill_info['room']}.pdf")
        page.snack_bar = ft.SnackBar(ft.Text("📄 พิมพ์ไฟล์ PDF สำเร็จ!"))
        page.snack_bar.open = True
        page.update()

    btn_pdf = ft.ElevatedButton("📄 พิมพ์ใบแจ้งหนี้ PDF", on_click=print_pdf, disabled=True, width=300)

    meter_pg = ft.Column([
        ft.Text("บันทึกค่ามิเตอร์", size=22),
        m_room, m_water, m_elec,
        ft.ElevatedButton("คำนวณยอดเงิน", on_click=calculate, width=300, bgcolor="blue", color="white"),
        calc_res, btn_pdf,
        ft.TextButton("กลับ", on_click=lambda _: nav("menu"))
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, visible=False)

    page.add(ft.Container(content=ft.Column([login_pg, menu_pg, search_pg, repair_pg, meter_pg]), expand=True))

ft.app(target=main)