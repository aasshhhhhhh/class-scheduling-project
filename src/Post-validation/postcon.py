#ฟังก์ชันตรวจสอบหลัง assign
def validate_final_timetable(timetable, instructors, time_slots, config):

    # สร้าง map slot → period, day
    slot_map = {t["slotId"]: {"day": t["day"], "period": t["period"]} for t in time_slots}


    # เก็บจำนวนชั่วโมงที่อาจารย์สอนทั้งหมด
    instructor_hours = {iid: 0 for iid in instructors.keys()}
  

    # เก็บจำนวนวิชาที่อาจารย์สอนแต่ละวัน
    instructor_courses_day = {
    iid: {d: set() for d in ["Monday","Tuesday","Wednesday","Thursday","Friday"]}
    for iid in instructors.keys()
    }
    
    # ตรวจทุกวัน ทุกช่องเวลา
    for day, slots in timetable.items(): 
      morning_courses = set() #สร้าง set
      afternoon_courses = set()

      for idx, cell in enumerate(slots): 

            # ถ้าเป็นช่องว่างหรือ Lunch
            if cell is None or cell == "Lunch Break":
                continue

            # cell มีรูปแบบ: "ENE100 (Dr.Somchai)"
            course_code = cell.split(" ")[0] 

            # ดึง instructorName จาก cell เพื่อค้น instructorId
            instructor_name = cell.split("(")[1].replace(")", "")
            instructor_id = None 
            for iid, info in instructors.items():
                if info["instructorName"] == instructor_name:
                    instructor_id = iid
                    break

            # หา slotId จาก time_slots mapping
            slotId = time_slots[idx]["slotId"] 
            period = slot_map[slotId]["period"]

            # --- ตรวจไม่เกิน 2 วิชา/เช้า หรือบ่าย ---
            if period == "morning":
                morning_courses.add(course_code)
            elif period == "afternoon":
                afternoon_courses.add(course_code)

            # --- นับจำนวนชั่วโมงที่อาจารย์สอน ---
            instructor_hours[instructor_id] += 1

            # --- ตรวจไม่เกิน 2 วิชา/วัน ---
            instructor_courses_day[instructor_id][day].add(course_code)

        # เช็คจำนวนวิชา/ช่วงเวลาในวันนั้น
            if len(morning_courses) > config["max_morning_courses"]:
              return False, f"ERROR: {day} มีวิชาช่วงเช้ามากกว่า 2 วิชา"

            if len(afternoon_courses) > config["max_afternoon_courses"]:
              return False, f"ERROR: {day} มีวิชาช่วงบ่ายมากกว่า 2 วิชา"

    # ==========================
    # ตรวจอาจารย์เกิน 2 วิชา/วัน
    # ==========================
    for iid, days in instructor_courses_day.items():
        for d, course_set in days.items():
            if len(course_set) > config["max_courses_per_day"]:
                return False, f"ERROR: {instructors[iid]['instructorName']} สอนเกิน 2 วิชาในวัน {d}"

    # ==========================
    # ตรวจอาจารย์เกิน 15 ชั่วโมง/สัปดาห์
    # ==========================
    for iid, total_hours in instructor_hours.items():
        if total_hours > config["max_hours_per_week"]:
            return False, f"ERROR: {instructors[iid]['instructorName']} สอนเกิน 15 ชม./สัปดาห์"

    # ==========================
    # ตรวจห้ามสอนใน forbidden slot
    # ==========================
    forbidden_slots = {t["slotId"] for t in time_slots if t["forbidden"]}

    for day, slots in timetable.items():
        for idx, cell in enumerate(slots):

            if not cell or cell == "Lunch Break":
                continue

            slotId = time_slots[idx]["slotId"]
            if slotId in forbidden_slots:
                return False, f"ERROR: มีการลงเรียนใน forbidden slot ({day}, slot {slotId})"

    return True, "✓ ตารางเรียนผ่านทุกเงื่อนไข"
