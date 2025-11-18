import os
import sys

# --- 1. แก้ไข Path ---
# ได้ .../Project_Root/test
current_dir = os.path.dirname(os.path.abspath(__file__))
# ได้ .../Project_Root
project_root = os.path.dirname(current_dir) 


# --- 2. แก้ไข Imports (ตอนนี้ Python จะหาเจอแล้ว) ---

from input_handler import load_data
from output_formatter import OutputFormatter
from scheduler import Scheduler # <-- ⭐️ 1. เพิ่ม Import นี้

def output_schedule():
    """ทดสอบ Output Formatter ด้วยข้อมูลจริงจาก JSON"""
    print("🧪 ทดสอบ Output Formatter ด้วยข้อมูลจริง")
    print("=" * 50)
    
    try:
        # --- 3. แก้ไข Path ของ data.json ---
        # สร้าง Path แบบเต็มไปยัง data.json โดยอิงจาก Project Root
        data_path = os.path.join(project_root, "data", "data.json")
        
        print(f"Loading data from: {data_path}")
        schedule = load_data(data_path)
        
        # --- ⭐️ 2. เพิ่มขั้นตอนการจัดตาราง (สำคัญมาก) ⭐️ ---
        print("\n⚙️ Running auto-scheduler...")
        scheduler = Scheduler(schedule) # สร้างเครื่องจัดตาราง
        scheduler.auto_schedule()       # สั่งรันการจัดตาราง (เติมข้อมูลลงใน schedule)
        print("✅ Scheduling complete.")
        # --- ⭐️ สิ้นสุดส่วนที่เพิ่ม ⭐️ ---
        
        # 3. ตอนนี้ schedule มีข้อมูลที่จัดแล้ว ส่งไปพิมพ์ได้
        formatter = OutputFormatter(schedule)
        
        # วนลูป 1, 2, 3, 4
        for year_to_display in range(1, 5): 
            formatter.display_schedule_by_year(year_to_display)
        
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        print("📌 สาเหตุอาจมาจาก:")
        print(f"   - หาไฟล์ data.json ไม่เจอที่: {data_path}")
        print("   - Data Structure (src/data_structures.py) ไม่ครบถ้วน")
        print("   - Input Handler (src/input_handler.py) มีปัญหา")

output_schedule()