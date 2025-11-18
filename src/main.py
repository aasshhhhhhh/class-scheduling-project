import os

# ตั้งค่า Path เพื่อให้หาไฟล์เจอ ไม่ว่าจะรันจากไหน 
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) 

# นำฟังก์ชันเข้าจากไฟล์อื่น (Module) ในโปรเจกต์
from input_handler import load_data
from output_formatter import OutputFormatter
from scheduler import Scheduler 


"""
    โหลดข้อมูลตารางเรียน → รันตัวจัดตารางอัตโนมัติ → แสดงผลตารางเรียนของทุกชั้นปี
"""
def output_schedule():
    try:
        data_path = os.path.join(project_root, "data", "data.json")
        print(f"Loading data from: {data_path}")


        # INPUT: โหลดข้อมูลดิบเข้าสู่ตัวแปร schedule
        schedule = load_data(data_path) 

        
        print("\n⚙️ Running auto-scheduler...")
        # PROCESS: เรียกใช้ Scheduler เพื่อจัดตารางเรียน
        scheduler = Scheduler(schedule) 
        scheduler.auto_schedule()       
        print("✅ Scheduling complete.")


        # OUTPUT: แสดงตารางเรียนที่ผ่านการจัดเรียบร้อยแล้ว
        formatter = OutputFormatter(schedule) 
        
        for year_to_display in range(1, 5): # วนลูปแสดงตารางเรียนทีละชั้นปี (ปี 1 ถึง ปี 4)
            formatter.display_schedule_by_year(year_to_display)
        
    except Exception as e: 
        # ดักจับ Error: ถ้าโปรแกรมพัง จะกระโดดมาทำตรงนี้แทนที่จะปิดตัวเองทันที
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        

output_schedule()