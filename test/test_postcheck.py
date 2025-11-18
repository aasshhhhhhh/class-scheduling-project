# test_postcheck.py (Corrected)

import os
import sys

# 1. ตั้งค่า PYTHONPATH เพื่อให้สามารถ import ไฟล์ใน src ได้
current_dir = os.path.dirname(os.path.abspath(__file__))

constraints_path = os.path.join(current_dir, "..", "constraints") 

if constraints_path not in sys.path:
    sys.path.append(constraints_path)

src_path = os.path.join(current_dir, "..", "src")
if src_path not in sys.path:
    sys.path.append(src_path)

# 2. Import ฟังก์ชันที่จำเป็น
# ... (ใน test_postcheck.py)
try:
    from input_handler import load_data
    # 💡 การแก้ไขที่ถูกต้องเมื่อสร้าง __init__.py แล้ว
    from constraints.postcheck import validate_post_schedule 
    from scheduler import Scheduler 
except ImportError as e:
# ...
    print(f"❌ Cannot import necessary modules: {e}")
    sys.exit(1)

def setup_real_schedule():
    """โหลด Schedule จาก data.json จริง"""
    data_path = os.path.join(current_dir, "..", "data", "data.json")
    try:
        # โหลดข้อมูล (schedule คือ Schedule object)
        schedule = load_data(data_path)
    except FileNotFoundError:
        print(f"❌ Error: Data file not found at {data_path}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Error during data loading/validation: {e}")
        sys.exit(1)

    # รัน auto_schedule เพื่อให้มี course.scheduled_slots สำหรับการทดสอบจริง
    print("\n--- Running Auto-Scheduler for Test Data ---")
    # ใช้ Scheduler ที่เพิ่งโหลดข้อมูลมา
    my_scheduler = Scheduler() 
    # 💡 FIX 2: ต้องกำหนด Schedule object เข้าไปใน Scheduler object
    my_scheduler.schedule = schedule 
    my_scheduler.auto_schedule(use_backtracking=True)

    # ส่งคืน Scheduler Object (my_scheduler) ที่ถูกจัดตารางแล้ว
    return my_scheduler 


def prepare_timetable_data(schedule):
    """
    สร้าง timetable (day -> list of cells) และ time_slots list
    ซึ่งเป็น format ที่ฟังก์ชัน validate_post_schedule ต้องการ
    """
    # 💡 FIX 3: schedule ที่ส่งเข้ามาคือ Scheduler object ต้องดึง Schedule object จริงด้วย .schedule
    actual_schedule = schedule.schedule 
    
    timetable = {}
    time_slots_list = []

    for day in ['Monday','Tuesday','Wednesday','Thursday','Friday']:
        timetable[day] = []

    # เรียงลำดับ TimeSlots ตาม ID เพื่อให้แน่ใจว่ามันเรียงตาม index ที่ถูกต้อง
    sorted_slots = sorted(actual_schedule.time_slots.values(), key=lambda x: x.slot_id)

    for slot in sorted_slots:
        # 1. เตรียม time_slots list
        time_slots_list.append({
            "slotId": slot.slot_id,
            "day": slot.day,
            "period": slot.period,
            "forbidden": getattr(slot, "forbidden", False)
        })

        # 2. หา course ใน slot นี้เพื่อสร้าง cell value
        cell_value = None
        for course in actual_schedule.courses.values():
            if slot.slot_id in course.scheduled_slots:
                instructor_name = actual_schedule.instructors[course.instructorId].instructorName
                cell_value = f"{course.course_code} ({instructor_name})"
                break

        # ถ้าเป็นช่วง lunch
        if slot.time == actual_schedule.config.lunch_break:
            cell_value = "Lunch Break"

        # เพิ่ม cell เข้าไปในตารางเรียนของวันนั้น
        timetable[slot.day].append(cell_value)

    # 3. เตรียม instructors และ config ในรูปแบบ dict
    instructors = {iid: {"instructorName": ins.instructorName} 
                   for iid, ins in actual_schedule.instructors.items()}
    config_dict = actual_schedule.config.__dict__

    return timetable, time_slots_list, instructors, config_dict


if __name__ == "__main__":
    print("--- Starting Post-Schedule Validation Test ---")
    
    # 1. Setup และรัน Auto Scheduler
    my_scheduled_data = setup_real_schedule()
    
    # 2. เตรียมข้อมูลสำหรับ validation
    # my_scheduled_data คือ Scheduler object
    timetable, time_slots_list, instructors, config_dict = prepare_timetable_data(my_scheduled_data)
    
    # 3. เรียก validate_post_schedule
    print("\n--- Running validate_post_schedule ---")
    # สังเกตลำดับ Argument: timetable, time_slots_list, instructors, config_dict
    valid, msg = validate_post_schedule(timetable, instructors, time_slots_list, config_dict)
    
    # 4. แสดงผลลัพธ์
    print("\n--- Test Result ---")
    if valid:
        print(f"✅ Post-schedule validation successful: {msg}")
    else:
        print(f"❌ Post-schedule validation failed: {msg}")
        sys.exit(1)
        
    print("---------------------")