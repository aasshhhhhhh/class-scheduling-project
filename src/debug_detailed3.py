# src/debug_detailed.py
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from input_handler import load_data
from scheduler import Scheduler

def debug_detailed():
    print("🐛 Debug Algorithm แบบละเอียด")
    print("=" * 50)
    
    schedule = load_data("./data/data.json")
    scheduler = Scheduler(schedule)
    
    # ทดสอบกับวิชาแรก
    first_course = list(schedule.courses.values())[0]
    instructor = schedule.instructors.get(first_course.instructorId)
    
    print(f"🧪 ทดสอบกับวิชาแรก: {first_course.course_code}")
    print(f"   - อาจารย์: {instructor.instructorName}")
    print(f"   - ต้องการ: {first_course.study_hours} ชั่วโมง")
    print(f"   - Priority: {first_course.priority}")
    
    # ทดสอบหา slots
    print(f"\n🔍 ทดสอบหา slots...")
    slot_ids = scheduler.find_continuous_slots(first_course.instructorId, first_course.study_hours)
    print(f"   - หา slots ได้: {slot_ids}")
    
    if slot_ids:
        print(f"   - ตรวจสอบเงื่อนไข can_assign...")
        can_assign = scheduler.can_assign(instructor, first_course, slot_ids)
        print(f"   - can_assign คืนค่า: {can_assign}")
        
        if can_assign:
            print(f"   - 🚀 พยายามจัดวิชา...")
            success = scheduler.assign_course(first_course, instructor, slot_ids)
            print(f"   - assign_course คืนค่า: {success}")
            
            if success:
                print(f"   - ✅ จัดวิชาสำเร็จ!")
                print(f"   - Slots ที่จัด: {first_course.scheduled_slots}")
            else:
                print(f"   - ❌ assign_course ล้มเหลว")
        else:
            print(f"   - ❌ can_assign ไม่ผ่าน")
            
            # Debug เงื่อนไข
            print(f"\n🔍 Debug เงื่อนไข can_assign:")
            print(f"   - ชั่วโมงสอนแล้ว: {instructor.assigned_hours}")
            print(f"   - ชั่วโมงที่จะเพิ่ม: {first_course.study_hours}")
            print(f"   - สูงสุดต่อสัปดาห์: {instructor.max_weekly_hours}")
            print(f"   - วิชาที่สอนแล้ว: {instructor.assigned_courses}")
    else:
        print(f"   - ❌ ไม่พบ slots")
    
    # ตรวจสอบผล
    assigned = sum(1 for c in schedule.courses.values() if c.scheduled_slots)
    print(f"\n📊 สรุป: จัดได้ {assigned} วิชา")

if __name__ == "__main__":
    debug_detailed()