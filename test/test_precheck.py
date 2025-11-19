import os
import sys
import copy

print("\n✅ ... RUNNING FINAL VERSION (5 CASES) ...\n")

# --- 1. Setup Paths ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
src_path = os.path.join(parent_dir, "src")

if src_path not in sys.path:
    sys.path.append(src_path)

try:
    from input_handler import load_data
    from constraints.precheck import check_assign_rules
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

def get_real_data():
    data_path = os.path.join(parent_dir, "data", "data.json")
    return load_data(data_path)

def find_slots(time_slots_map, day, period, count):
    found_ids = []
    for sid, slot in time_slots_map.items():
        if slot.day == day and slot.period == period and not slot.forbidden:
            found_ids.append(sid)
            if len(found_ids) >= count:
                break
    return found_ids

def run_all_tests():
    print("="*60)
    print(" 🧪 STARTING FINAL PRECHECK TESTS ")
    print("="*60)
    
    # Load Data
    schedule_obj = get_real_data()
    config = schedule_obj.config
    time_slots_map = schedule_obj.time_slots
    
    target_course = schedule_obj.courses.get("ENE100") or list(schedule_obj.courses.values())[0]
    instructor = schedule_obj.instructors[target_course.instructorId]
    
    print(f"📝 Subject: {target_course.course_code}")
    print(f"👨‍🏫 Instructor: {instructor.instructorName}")
    
    test_slot_ids = find_slots(time_slots_map, "Monday", "morning", target_course.study_hours)

    # --- CASE 1: Normal ---
    print("\n🔹 Case 1: Normal Assignment (Happy Path)")
    instructor.assigned_hours = 0
    instructor.assigned_courses = []
    res = check_assign_rules(instructor, target_course, test_slot_ids, time_slots_map, {}, config)
    print(f"   Result: {'✅ PASS' if res else '❌ FAIL'}")

    # --- CASE 2: Morning Full ---
    print(f"\n🔹 Case 2: Morning Quota Full ({config.max_morning_courses} courses)")
    sim_schedule = { "Monday": {} }
    m_slots = [s for s in time_slots_map.values() if s.day == "Monday" and s.period == "morning"]
    for i in range(min(len(m_slots), config.max_morning_courses)):
        sim_schedule["Monday"][m_slots[i].time] = f"FAKE_{i}"
            
    res = check_assign_rules(instructor, target_course, test_slot_ids, time_slots_map, sim_schedule, config)
    print(f"   Result: {'✅ BLOCKED (Correct)' if not res else '❌ ALLOWED (Wrong)'}")

    # --- CASE 3: Daily Limit ---
    print(f"\n🔹 Case 3: Instructor Daily Limit ({instructor.max_daily_courses} courses)")
    instructor.assigned_courses = [] 
    mon_slots = [sid for sid, s in time_slots_map.items() if s.day == "Monday" and not s.forbidden]
    for i in range(instructor.max_daily_courses):
        if i < len(mon_slots):
            d = copy.deepcopy(target_course)
            d.course_code = f"DUMMY_{i}"
            d.scheduled_slots = [mon_slots[i]]
            instructor.assigned_courses.append(d)
            
    res = check_assign_rules(instructor, target_course, test_slot_ids, time_slots_map, {}, config)
    print(f"   Result: {'✅ BLOCKED (Correct)' if not res else '❌ ALLOWED (Wrong)'}")

    # --- CASE 4: Afternoon Full (ที่เพิ่มเข้ามา) ---
    print(f"\n🔹 Case 4: Afternoon Quota Full ({config.max_afternoon_courses} courses)")
    test_day = "Thursday"
    pm_slots = find_slots(time_slots_map, test_day, "afternoon", target_course.study_hours)
    
    if pm_slots:
        sim_pm = { test_day: {} }
        pm_all = [s for s in time_slots_map.values() if s.day == test_day and s.period == "afternoon"]
        for i in range(min(len(pm_all), config.max_afternoon_courses)):
            sim_pm[test_day][pm_all[i].time] = f"FAKE_PM_{i}"
        
        instructor.assigned_courses = []
        instructor.assigned_hours = 0
        res = check_assign_rules(instructor, target_course, pm_slots, time_slots_map, sim_pm, config)
        print(f"   Result: {'✅ BLOCKED (Correct)' if not res else '❌ ALLOWED (Wrong)'}")
    else:
        print("   ⚠️ Skip: No afternoon slots found for testing.")

    # --- CASE 5: Max Weekly Hours (ที่เพิ่มเข้ามา) ---
    print(f"\n🔹 Case 5: Max Weekly Hours ({instructor.max_weekly_hours} hrs)")
    instructor.assigned_courses = []
    instructor.assigned_hours = 14 # สมมติสอนแล้ว 14 ชม.
    
    print(f"   Current: 14 hrs + New: {target_course.study_hours} hrs = {14 + target_course.study_hours} hrs")
    res = check_assign_rules(instructor, target_course, test_slot_ids, time_slots_map, {}, config)
    print(f"   Result: {'✅ BLOCKED (Correct)' if not res else '❌ ALLOWED (Wrong)'}")

    print("\n" + "="*60)

if __name__ == "__main__":
    run_all_tests()