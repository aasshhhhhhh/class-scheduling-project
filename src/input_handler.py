import os
import json
from data_structures import Schedule, Config

def load_data(json_file_path):
    """
    โหลดข้อมูลจาก JSON, สร้างอ็อบเจกต์ Schedule และทำการตรวจสอบความถูกต้อง
    """
    try:
        with open(json_file_path, "r", encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ File '{json_file_path}' not found")
    except json.JSONDecodeError:
        raise ValueError(f"❌ File '{json_file_path}' is not a valid JSON")
    
    schedule = Schedule()
    
    # 1. โหลด Config ก่อน
    config_data = data.get('config', {})
    schedule.config = Config(**config_data)

    # 2. โหลด TimeSlots
    for time_slot_data in data.get('time_slots', []):
        schedule.add_time_slot(**time_slot_data)
        
    # 3. โหลด Instructors
    for instructor_data in data.get('instructors', []):
        schedule.add_instructor(**instructor_data)
        
    # 4. โหลด Courses
    for course_data in data.get('courses', []):
        schedule.add_course(**course_data)
    
    # 5. ตรวจสอบความถูกต้อง
    validate_data(schedule)
    
    return schedule

def validate_data(schedule):
    """
    ตรวจสอบความถูกต้องของข้อมูลที่โหลดเข้าสู่ Schedule object
    """
    errors = []

    # ตรวจสอบ Instructor ID ของ Course
    instructor_ids = set(schedule.instructors.keys())
    for course_code, course in schedule.courses.items():
        if course.instructorId not in instructor_ids:
            errors.append(f"Instructor ID '{course.instructorId}' not found for course '{course_code}'")

    # ตรวจสอบ Slot ID ไม่ซ้ำ
    slot_ids = list(schedule.time_slots.keys())
    if len(slot_ids) != len(set(slot_ids)):
        # อันนี้อาจไม่จำเป็นถ้า TimeSlot ถูกเพิ่มโดยใช้ keys ของ dict
        errors.append("Duplicate slot_id found in time_slots data before loading.")

    # ตรวจสอบ forbidden slots ของอาจารย์ 
    # (ใช้ schedule.config.forbidden_slot ที่เราสร้างไว้ใน data_structures.py)
    forbidden_ids = set(schedule.config.forbidden_slot)
    for ins_id, ins in schedule.instructors.items():
        # ตรวจสอบว่า available_slots ที่อาจารย์กำหนดไว้ทับซ้อนกับ forbidden_ids หรือไม่
        overlap = forbidden_ids.intersection(ins.available_slots)
        if overlap:
            errors.append(f"Instructor '{ins.instructorName}' ({ins_id}) is available in forbidden slots: {list(overlap)}")
            
    # ตรวจสอบว่า slot_id ใน available_slots ของอาจารย์มีอยู่ใน time_slots จริงหรือไม่
    valid_slot_ids = set(schedule.time_slots.keys())
    for ins_id, ins in schedule.instructors.items():
        invalid_slots = set(ins.available_slots) - valid_slot_ids
        if invalid_slots:
             errors.append(f"Instructor '{ins.instructorName}' ({ins_id}) has invalid available slots: {list(invalid_slots)}")

    # แสดงผลลัพธ์
    if errors:
        print("❌ Validation Errors:")
        for e in errors:
            print("  -", e)
        # หากมี error ให้ยกเลิกการทำงาน
        raise ValueError("Data validation failed. See errors above.")
    else:
        print("✅ All data validated successfully!")