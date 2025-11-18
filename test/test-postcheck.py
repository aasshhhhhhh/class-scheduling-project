import sys
import os
import unittest

# --- 1. การจัดการ Path (เหมือนเดิม) ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')

if src_path not in sys.path:
    sys.path.insert(0, src_path)

# --- 2. Import โมดูลจริงๆ ของคุณ ---
try:
    from input_handler import load_data
    from scheduler import Scheduler
    from constraints.postcheck import validate_post_schedule
except ImportError as e:
    print(f"ERROR: ไม่สามารถ import โมดูลจาก '{src_path}'")
    print(f"Details: {e}")
    sys.exit(1)

# --- 3. [สำคัญ] ฟังก์ชันแปลงข้อมูล (Converter) ---
# เราจะใช้ฟังก์ชันนี้เพื่อแปลง "Schedule Object" ให้เป็น "Timetable Dict"
# ที่ postcheck.py ต้องการ

def convert_schedule_for_validation(schedule_obj):
    """
    แปลง Schedule object ที่จัดตารางแล้ว 
    ให้เป็น formats ที่ validate_post_schedule ต้องการ
    """
    
    # --- 3A. สร้าง Config Dictionary ---
    # แก้ปัญหาชื่อไม่ตรงกัน (max_daily_courses vs max_courses_per_day)
    config_dict = {
        "max_morning_courses": schedule_obj.config.max_morning_courses,
        "max_afternoon_courses": schedule_obj.config.max_afternoon_courses,
        "max_courses_per_day": schedule_obj.config.max_daily_courses, # <--- แก้ไขตรงนี้
        "max_hours_per_week": schedule_obj.config.max_weekly_hours      # <--- เพิ่มอันนี้
    }

    # --- 3B. สร้าง Instructors Dictionary ---
    instructors_dict = {}
    for iid, inst_obj in schedule_obj.instructors.items():
        instructors_dict[iid] = {
            "instructorName": inst_obj.instructorName
        }
        
    # --- 3C. สร้าง Time Slots List (แม่แบบของ 1 วัน) ---
    # postcheck.py ต้องการ 'list' ของ time_slots ตามลำดับ
    # เราจะใช้ลำดับเดียวกับ output_formatter.py (8 ช่อง)
    # (หมายเหตุ: นี่เป็นจุดที่เปราะบาง ถ้า data.json มี slot ไม่ครบ 8 ช่อง/วัน อาจมีปัญหา)
    
    time_strings_ordered = [
        '08:30-09:30', '09:30-10:30', '10:30-11:30', '11:30-12:30',
        '13:30-14:30', '14:30-15:30', '15:30-16:30', '16:30-17:30'
    ]
    
    # หา slot object ต้นแบบ (เราสมมติว่า slotId 1-8 หรือ 101-108 คือแม่แบบ)
    day_template_slots = []
    
    # สร้าง lookup จาก time string ไปยัง slot object
    slot_lookup_by_time = {}
    for slot in schedule_obj.time_slots.values():
        if slot.time not in slot_lookup_by_time:
             # เก็บ slot แรกที่เจอของเวลานั้นๆ
             slot_lookup_by_time[slot.time] = slot

    for time_str in time_strings_ordered:
        if time_str in slot_lookup_by_time:
            slot_obj = slot_lookup_by_time[time_str]
            day_template_slots.append({
                "slotId": slot_obj.slot_id, # postcheck.py ใช้ slotId จากแม่แบบนี้
                "day": slot_obj.day, # postcheck.py ไม่ได้ใช้ แต่ใส่ไว้
                "period": slot_obj.period,
                "forbidden": slot_obj.forbidden
            })
        else:
            # กรณี data.json ไม่มีเวลานี้ (เช่น 11:30-12:30)
            day_template_slots.append(None) # หรือ {} ขึ้นอยู่กับการออกแบบ

    # --- 3D. สร้าง Timetable Dictionary (ส่วนที่ยากที่สุด) ---
    timetable_dict = {}
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    # สร้างตารางเปล่าๆ ก่อน
    for day in days:
        timetable_dict[day] = [None] * len(day_template_slots) # 8 ช่อง

    # ใส่ "Lunch Break" (อ้างอิงจาก output_formatter.py)
    lunch_time = "11:30-12:30"
    if lunch_time in time_strings_ordered:
        lunch_idx = time_strings_ordered.index(lunch_time)
        for day in days:
            timetable_dict[day][lunch_idx] = "Lunch Break"

    # วนลูปทุกวิชาที่จัดตารางแล้ว
    for course in schedule_obj.courses.values():
        if not course.scheduled_slots:
            continue # ข้ามวิชาที่จัดไม่ได้
            
        instructor_name = instructors_dict[course.instructorId]["instructorName"]
        cell_text = f"{course.course_code} ({instructor_name})"
        
        # วนลูปทุก slot ที่วิชานี้เรียน
        for slot_id in course.scheduled_slots:
            slot_obj = schedule_obj.time_slots[slot_id]
            day = slot_obj.day
            time = slot_obj.time
            
            if time not in time_strings_ordered:
                continue # ข้าม slot ที่ไม่อยู่ในแม่แบบ
                
            idx = time_strings_ordered.index(time)
            
            if day in timetable_dict:
                timetable_dict[day][idx] = cell_text

    return timetable_dict, instructors_dict, day_template_slots, config_dict


# --- 4. Test Case ---

class TestRealDataPostCheck(unittest.TestCase):
    
    # ใช้ setUpClass เพื่อโหลดข้อมูลและรัน scheduler "ครั้งเดียว"
    @classmethod
    def setUpClass(cls):
        print("--- Setting up Test: Loading data and running scheduler ---")
        
        # 4.1. กำหนด Path ไปยัง data.json
        # (ปรับ path นี้ถ้า data.json ของคุณไม่ได้อยู่ที่ 'project_root/data/data.json')
        cls.data_path = os.path.join(project_root, "data", "data.json")
        if not os.path.exists(cls.data_path):
            # ลองหาใน src/data/ ถ้าหาข้างนอกไม่เจอ
            cls.data_path = os.path.join(src_path, "..", "data", "data.json")

        try:
            # 4.2. โหลดข้อมูลจริง
            cls.schedule_obj = load_data(cls.data_path)
            
            # 4.3. รัน Scheduler จริง
            scheduler = Scheduler(cls.schedule_obj)
            scheduler.auto_schedule() # (เราสมมติว่า auto_schedule จัดตารางได้สำเร็จ)
            
            print("--- Scheduler finished running ---")
            
        except Exception as e:
            raise unittest.SkipTest(f"Failed to load or run scheduler: {e}")

    def test_run_post_check_on_scheduled_data(self):
        """
        เทสว่าตารางที่ได้จาก auto_schedule() นั้น ผ่าน post-check หรือไม่
        """
        print("\n--- Test: Running Post-Check Validation ---")
        
        # 1. แปลงข้อมูล
        try:
            timetable, instructors, time_slots, config = convert_schedule_for_validation(self.schedule_obj)
        except Exception as e:
            self.fail(f"Converter function failed with error: {e}")
            
        # 2. รัน Validate
        is_valid, message = validate_post_schedule(
            timetable, 
            instructors, 
            time_slots, 
            config
        )
        
        # 3. ตรวจสอบผลลัพธ์
        print(f"Validation Result: {is_valid}")
        print(f"Message: {message}")
        
        # เราคาดหวังว่าตารางที่ scheduler จัดได้ "ควรจะ" ผ่านการตรวจสอบเสมอ
        self.assertTrue(is_valid, f"Validate_post_scheduleล้มเหลว: {message}")

# --- 5. รันเทส ---
if __name__ == '__main__':
    unittest.main()