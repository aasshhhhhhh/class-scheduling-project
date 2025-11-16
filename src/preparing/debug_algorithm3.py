# src/debug_algorithm.py
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from input_handler import load_data
from scheduler import Scheduler

def debug_algorithm():
    print("🐛 Debug Algorithm ของคนที่ 3")
    print("=" * 50)
    
    schedule = load_data("./data/data.json")
    
    # ตรวจสอบข้อมูลเบื้องต้น
    print(f"📚 วิชาทั้งหมด: {len(schedule.courses)} วิชา")
    print(f"👨‍🏫 อาจารย์: {len(schedule.instructors)} คน")
    print(f"⏰ ช่วงเวลา: {len(schedule.time_slots)} ช่วง")
    
    # ตรวจสอบวิชาตัวอย่าง
    print(f"\n🔍 ตรวจสอบวิชาตัวอย่าง:")
    for i, (code, course) in enumerate(list(schedule.courses.items())[:3]):
        instructor = schedule.instructors.get(course.instructorId)
        instructor_name = instructor.instructorName if instructor else "ไม่พบ"
        print(f"   {i+1}. {code} (ปี{course.year}, {course.study_hours}ชม.) - {instructor_name}")
    
    # ตรวจสอบอาจารย์ตัวอย่าง
    print(f"\n🔍 ตรวจสอบอาจารย์ตัวอย่าง:")
    for i, (id, instructor) in enumerate(list(schedule.instructors.items())[:3]):
        print(f"   {i+1}. {instructor.instructorName}: {len(instructor.available_slots)} slots")
    
    # รัน Algorithm แบบ verbose
    print(f"\n🔄 รัน Algorithm แบบละเอียด...")
    scheduler = Scheduler(schedule)
    
    # ตรวจสอบ method find_continuous_slots
    print(f"\n🧪 ทดสอบ find_continuous_slots:")
    test_instructor = list(schedule.instructors.keys())[0]
    test_slots = scheduler.find_continuous_slots(test_instructor, 3)
    print(f"   อาจารย์ {test_instructor} หา 3 slots ต่อเนื่องได้: {test_slots}")
    
    # รัน Algorithm
    scheduler.auto_schedule(use_backtracking=True)
    
    # ตรวจสอบผลลัพธ์
    assigned_courses = [c for c in schedule.courses.values() if c.scheduled_slots]
    print(f"\n📊 ผลลัพธ์:")
    print(f"   วิชาที่ถูกจัดแล้ว: {len(assigned_courses)} วิชา")
    
    if assigned_courses:
        print(f"   วิชาที่จัดได้:")
        for course in assigned_courses[:5]:  # แสดง 5 วิชาแรก
            print(f"     - {course.course_code} ({len(course.scheduled_slots)} slots)")
    else:
        print(f"   ❌ ไม่มีวิชาถูกจัดเลย!")

if __name__ == "__main__":
    debug_algorithm()