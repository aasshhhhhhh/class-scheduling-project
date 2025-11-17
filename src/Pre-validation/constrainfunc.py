#ให้ greedy ใช้
def can_assign_precheck(course, day, start_idx, duration, timetable, instructor, time_slots, config):
    """
    ตรวจสอบว่า course สามารถวางในช่วงเวลา [start_idx, start_idx+duration) ได้หรือไม่
    (ใช้ก่อน greedy จะทำการวาง)
    """
    course_code = course["course_code"] #ดึงรหัสวิชาออกมาจากข้อมูลวิชาแต่ละตัว เช่น "MTH101", "GEN111"
    instructorId = course["instructorId"] #ดึงรหัสอาจารย์ที่สอนวิชานั้น เช่น "T01", "T07"
    period_count = {"morning": set(), "afternoon": set()} #สร้างตัวแปรเก็บข้อมูลว่า “อาจารย์ใช้ไปแล้วกี่คาบในตอนเช้าและตอนบ่าย”

    # -----------------------------
    # 1) ห้ามชนกับคาบที่มีอยู่แล้ว
    # -----------------------------้
    for i in range(start_idx, start_idx + duration): #วนตรวจ ทุก index ตั้งแต่เวลาเริ่ม (start_idx) ไปจนถึงจำนวนชั่วโมงที่ต้องใช้ (duration)
    # ❌ ห้ามจองช่วง Lunch Break
      if timetable[i] == "Lunch Break":
        return False
    # ❌ ห้ามจองถ้ามีวิชาอยู่แล้ว (ไม่ชนนักศึกษา)
      if timetable[i] is not None:
        return False
    # -----------------------------
    # 2) slot ต้องไม่ Forbidden (ห้าม อาจารย์ไม่เกิน 15 ชมต่อสัปดาห์, อาจารย์ไม่เกิน 2 วิชาต่อวัน, Monday afternoon, เช้าบ่ายไม่เกิน 2 วิชา, พักกลางวัน)
    # -----------------------------
    slot_ids = [time_slots[i]["slotId"] for i in range(start_idx, start_idx + duration)]
    if any(sid in config["forbidden_slot_ids"] for sid in slot_ids):
        return False
  #ถ้า slot ไหนก็ตาม (ในช่วงเวลาที่กำลังพิจารณา) ไปตรงกับรายการช่องเวลาที่ห้ามจอง (forbidden_slot_ids) → คืนค่า False (จองไม่ได้)

    # -----------------------------
    # 3) วิชาต้องมีช่วงเวลาเรียงต่อเนื่อง
    # (โดย greedy ใช้ duration แบบต่อเนื่องอยู่แล้ว)
    # -----------------------------
    # ไม่ต้องเช็คเพิ่ม เพราะ greedy จะกำหนด duration เอง

    # -----------------------------
    # 4) 1 คาบเรียนไม่เกิน 3 ชั่วโมง
    # -----------------------------
    if duration > 3:
        return False

    # -----------------------------
    # 5) จำกัดวิชาเช้า/บ่าย ไม่เกิน 2 วิชา/ครึ่งวัน
    # -----------------------------
    for i in range(len(timetable)):
        s = timetable[i]
        if s and s not in [None, "Lunch Break"]:
            period = time_slots[i]["period"] #ดึงช่วงเวลา period ของคาบนั้น ("morning" หรือ "afternoon") จาก time_slots ใช้เพื่อนับจำนวนวิชาในแต่ละช่วง
            code = s.split("(")[0]  # ตัดเอาเฉพาะรหัสวิชา เช่น "ENE100" โดยตัดชื่ออาจารย์ออก
            period_count[period].add(code) #นับจำนวนวิชาในเช้า/บ่าย เพื่อเช็ค constraint “เช้า/บ่ายไม่เกิน 2 วิชา”

    # นับคาบใหม่ว่าคาบนี้เป็นเช้า/บ่าย
    new_period = time_slots[start_idx]["period"] #เอาช่วงเวลาของ slot ที่กำลังพิจารณา (start_idx) ว่าเป็น "morning" หรือ "afternoon"
    period_count[new_period].add(course_code)

    if len(period_count["morning"]) > config["max_morning_courses"]:
        return False
    if len(period_count["afternoon"]) > config["max_afternoon_courses"]:
        return False

    # -----------------------------
    # 6) อาจารย์ว่างในทุก slot ที่จะสอน
    # -----------------------------
    available = set(instructor["available_slot"]) #แปลง list ของ slot ที่อาจารย์ว่างให้เป็น set เพื่อให้ตรวจสอบง่ายและเร็ว
    if not all(slot_ids[k] in available for k in range(len(slot_ids))): #slot_ids คือ list ของ slot ที่วิชานี้ต้องการ (เช่น ถ้าวิชาต้องเรียน 3 ชั่วโมง ก็มี 3 slot ต่อเนื่อง) เช็คทุก slot ว่าอยู่ใน available ของอาจารย์หรือไม่
#ถ้ามี slot ไหนอาจารย์ไม่ว่าง → คืนค่า False
        return False

    return True
