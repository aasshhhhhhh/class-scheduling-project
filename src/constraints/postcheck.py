def validate_post_schedule(timetable, instructors, time_slots, config):
    """
    Validates the entire schedule after all assignments are made (Post-check).
    """
    
    # Map slotId to its day and period
    slot_map = {t["slotId"]: {"day": t["day"], "period": t["period"]} for t in time_slots}

    # Track total hours per instructor
    instructor_hours = {iid: 0 for iid in instructors.keys()}
  
    # Track courses taught per day per instructor
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

            # --- Constraint: Max morning/afternoon courses per day ---
            if len(morning_courses) > config["max_morning_courses"]:
              # Changed error message to English
              return False, f"ERROR: {day} has more than {config['max_morning_courses']} morning courses"

            if len(afternoon_courses) > config["max_afternoon_courses"]:
              # Changed error message to English
              return False, f"ERROR: {day} has more than {config['max_afternoon_courses']} afternoon courses"

    # (โค้ดเดิม / Original code ... )

    # --- Constraint: Max courses per day (Instructor) ---
    for iid, days in instructor_courses_day.items():
        for d, course_set in days.items():
            if len(course_set) > config["max_daily_courses"]:
                # Changed error message to English
                return False, f"ERROR: {instructors[iid]['instructorName']} teaches more than {config['max_daily_courses']} courses on {d}"

    # --- Constraint: Max hours per week (Instructor) ---
    for iid, total_hours in instructor_hours.items():
        if total_hours > config["max_weekly_hours"]:
            # Changed error message to English
            return False, f"ERROR: {instructors[iid]['instructorName']} teaches over {config['max_weekly_hours']} hours/week"
        
    forbidden_slots = {t["slotId"] for t in time_slots if t["forbidden"]}

    for day, slots in timetable.items():
        for idx, cell in enumerate(slots):

            if not cell or cell == "Lunch Break":
                continue

            slotId = time_slots[idx]["slotId"]
            if slotId in forbidden_slots:
                return False, f"ERROR: มีการลงเรียนใน forbidden slot ({day}, slot {slotId})"


    # All checks passed
    return True, "Validation successful"