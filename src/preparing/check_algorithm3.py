# src/check_algorithm.py
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from input_handler import load_data
from scheduler import Scheduler  # ← ของคนที่ 3

def check_algorithm():
    print("🔍 ตรวจสอบ Algorithm ของคนที่ 3")
    
    schedule = load_data("./data/data.json")
    
    # นับก่อนรัน Algorithm
    before = sum(1 for c in schedule.courses.values() if c.scheduled_slots)
    print(f"📊 ก่อนรัน Algorithm: {before} วิชาที่ถูกจัดแล้ว")
    
    # รัน Algorithm ของคนที่ 3
    print("🔄 กำลังรัน Algorithm...")
    scheduler = Scheduler(schedule)
    scheduler.auto_schedule()
    
    # นับหลังรัน Algorithm  
    after = sum(1 for c in schedule.courses.values() if c.scheduled_slots)
    print(f"📊 หลังรัน Algorithm: {after} วิชาที่ถูกจัดแล้ว")
    
    if after > before:
        print("✅ Algorithm ทำงานได้")
    else:
        print("❌ Algorithm ไม่ทำงานหรือมีปัญหา")

if __name__ == "__main__":
    check_algorithm()