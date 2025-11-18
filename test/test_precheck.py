import os
import sys
import copy

# --- 1. ตั้งค่า Path (Setup Paths) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
src_path = os.path.join(parent_dir, "src")

# เพิ่มโฟลเดอร์ src เข้าไปใน system path เพื่อให้ Python หาไฟล์เจอ
if src_path not in sys.path:
    sys.path.append(src_path)

# --- 2. นำเข้าไลบรารี (Imports) ---
try:
    from input_handler import load_data
    # นำเข้า Schedule (ลบ Course ออกเพื่อไม่ให้ Editor แจ้งเตือนว่าไม่ได้ใช้)
    from data_structures import Schedule 
    
    # นำเข้าฟังก์ชันที่จะเทสจาก constraints.precheck
    from constraints.precheck import check_assign_rules
    
except ImportError as e:
    print(f"❌ เกิดข้อผิดพลาดในการนำเข้า (Import Error): {e}")
    print("คำแนะนำ: ตรวจสอบว่ามีไฟล์ __init__.py ในโฟลเดอร์ src/constraints/ หรือไม่")
    sys.exit(1)

def get_real_data():
    """โหลดข้อมูลจริงจากไฟล์ data.json"""
    data_path = os.path.join(parent_dir, "data", "data.json")
    print(f"📂 กำลังโหลดข้อมูลจริงจาก: {data_path}")
    try:
        schedule = load_data(data_path)
        return schedule
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")
        sys.exit(1)

def test_check_assign_rules():
    print("\n--- เริ่มต้นการทดสอบ: check_assign_rules (ใช้ข้อมูลจริง) ---")
    
    # 1. โหลดข้อมูลจริง
    schedule_obj = get_real_data()
    
    config = schedule_obj.config
    time_slots_map = schedule_obj.time_slots
    
    # 2. เลือกตัวอย่างข้อมูลมาทดสอบ (Simulation)
    if not schedule_obj.courses:
        print("❌ ไม่พบข้อมูลรายวิชาใน data.json")
        return

    # เลือกวิชาตัวแรกมาทดสอบ
    first_course_code = list(schedule_obj.courses.keys())[0]
    target_course = schedule_obj.courses[first_course_code]
    instructor = schedule_obj.instructors[target_course.instructorId]
    
    print(f"📝 กำลังทดสอบกับวิชา: {target_course.course_code} ({target_course.course_name})")
    print(f"👨‍🏫 อาจารย์ผู้สอน: {instructor.instructorName}")

    # เตรียม year_schedule ว่างๆ (สำหรับจำลองตารางเรียนของชั้นปี)
    year_schedule = {} 
    
    # หา Slot วันจันทร์เช้า เพื่อใช้ทดสอบ
    test_slot_ids = []
    for sid, slot in time_slots_map.items():
        if slot.day == "Monday" and slot.period == "morning":
            test_slot_ids.append(sid)
            if len(test_slot_ids) >= target_course.study_hours:
                break
                
    if not test_slot_ids:
        print("❌ ไม่พบช่วงเวลาที่เหมาะสมสำหรับการทดสอบ (ต้องเป็นเช้าวันจันทร์) โปรดตรวจสอบข้อมูลใน json")
        return

    print(f"🕒 กำลังพยายามลงเวลาใน slot IDs: {test_slot_ids} (เช้าวันจันทร์)")

    # ==========================================
    # กรณีทดสอบที่ 1: การลงทะเบียนปกติ (Happy Path)
    # ==========================================
    print("\n🔹 กรณีทดสอบที่ 1: การลงทะเบียนปกติ (ควรผ่าน)")
    
    # รีเซ็ตค่าอาจารย์ให้เหมือนเริ่มต้นใหม่
    instructor.assigned_hours = 0
    instructor.assigned_courses = []
    
    result = check_assign_rules(
        instructor=instructor, 
        course=target_course, 
        slot_ids=test_slot_ids, 
        time_slots_map=time_slots_map, 
        year_schedule=year_schedule, 
        config=config
    )
    
    if result:
        print("✅ ผ่าน: ระบบอนุญาตให้ลงทะเบียนได้ถูกต้อง")
    else:
        print("❌ ไม่ผ่าน: ระบบบล็อกการลงทะเบียนที่ควรจะทำได้")

    # ==========================================
    # กรณีทดสอบที่ 2: เกินขีดจำกัดวิชาเรียนช่วงเช้า
    # ==========================================
    print("\n🔹 กรณีทดสอบที่ 2: เกินขีดจำกัดวิชาช่วงเช้า (ไม่ควรผ่าน)")
    
    # จำลองว่าตารางเรียนเช้าวันจันทร์เต็มแล้ว
    simulated_year_schedule = { "Monday": {} }
    morning_slots = [s for s in time_slots_map.values() if s.day == "Monday" and s.period == "morning"]
    
    count = 0
    # สร้างวิชาปลอมๆ ใส่เข้าไปจนเกือบเต็ม หรือเต็มโควต้า
    for slot in morning_slots:
        if count < config.max_morning_courses:
            # ใส่ชื่อวิชาปลอมลงไปในเวลา
            simulated_year_schedule["Monday"][slot.time] = f"FAKE_COURSE_{count}"
            count += 1
            
    print(f"   จำลองตารางวันจันทร์: มีเรียนแล้ว {len(simulated_year_schedule['Monday'])} วิชา (ขีดจำกัด: {config.max_morning_courses})")
    
    result = check_assign_rules(
        instructor=instructor, 
        course=target_course, 
        slot_ids=test_slot_ids, 
        time_slots_map=time_slots_map, 
        year_schedule=simulated_year_schedule, 
        config=config
    )
    
    if not result:
        print("✅ ผ่าน: ระบบบล็อกเนื่องจากโควต้าช่วงเช้าเต็มแล้ว")
    else:
        print(f"❌ ไม่ผ่าน: ระบบอนุญาตให้ลงทะเบียนทั้งที่เกินขีดจำกัดช่วงเช้า ({config.max_morning_courses})")

    # ==========================================
    # กรณีทดสอบที่ 3: อาจารย์สอนเกินจำนวนวิชาต่อวัน
    # ==========================================
    print("\n🔹 กรณีทดสอบที่ 3: เกินขีดจำกัดสอนต่อวันของอาจารย์ (ไม่ควรผ่าน)")
    
    # เคลียร์ตารางเรียนปีให้ว่าง (เพื่อให้ผ่านเงื่อนไขข้อ 2 มาได้)
    year_schedule_clean = {}
    # รีเซ็ตวิชาที่อาจารย์สอน
    instructor.assigned_courses = [] 
    
    # ตรวจสอบว่ามี slot วันจันทร์พอให้สร้างวิชาหลอกไหม
    monday_slots_ids = [sid for sid, s in time_slots_map.items() if s.day == "Monday"]
    
    if len(monday_slots_ids) < instructor.max_daily_courses:
         print(f"⚠️ คำเตือน: ในข้อมูลมี Slot วันจันทร์ไม่เพียงพอที่จะทดสอบขีดจำกัดนี้ให้สมบูรณ์ (มี: {len(monday_slots_ids)}, ต้องการ: {instructor.max_daily_courses})")

    # สร้างวิชาหลอกๆ (Dummy Courses) ใส่ให้อาจารย์สอนจนเต็มโควต้าวันจันทร์
    for i in range(min(instructor.max_daily_courses, len(monday_slots_ids))):
        dummy_course = copy.deepcopy(target_course)
        dummy_course.course_code = f"DUMMY_{i}"
        
        # ดึง slot_id มาใช้ตรงๆ (เพราะ sid เป็น int อยู่แล้ว ไม่ต้อง .slot_id)
        mon_slot_id = monday_slots_ids[i] 
        
        dummy_course.scheduled_slots = [mon_slot_id]
        instructor.assigned_courses.append(dummy_course)
        
    print(f"   อาจารย์มีสอนแล้ว {len(instructor.assigned_courses)} วิชาในวันจันทร์ (ขีดจำกัด: {instructor.max_daily_courses})")
    
    result = check_assign_rules(
        instructor=instructor, 
        course=target_course, 
        slot_ids=test_slot_ids, 
        time_slots_map=time_slots_map, 
        year_schedule=year_schedule_clean, 
        config=config
    )
    
    if not result:
        print("✅ ผ่าน: ระบบบล็อกเนื่องจากอาจารย์สอนเกินขีดจำกัดต่อวัน")
    else:
        print(f"❌ ไม่ผ่าน: ระบบอนุญาตให้ลงทะเบียนทั้งที่อาจารย์สอนเกินขีดจำกัด ({instructor.max_daily_courses})")

if __name__ == "__main__":
    test_check_assign_rules()