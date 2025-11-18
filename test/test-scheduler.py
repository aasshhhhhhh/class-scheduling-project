# \test\test-scheduler.py

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..", "src")
if src_path not in sys.path:
    sys.path.append(src_path)

try:
    from scheduler import Scheduler
except ImportError:
    print(f"❌ Can not import 'scheduler' from: {src_path}")
    sys.exit(1)

my_scheduler = Scheduler()


# 2. ดึงข้อมูลวิชาแบบ Dynamic
print("--- Selecting a Course for Testing ---")
# โจทย์การเทส: เราต้องการวิชาที่เรียน 2 ชั่วโมง เพื่อทดสอบการหา Continuous Slots
desired_study_hours = 3
target_course = None

# วนลูปหาจากรายการวิชาทั้งหมด
for course in my_scheduler.courses.values():
    if course.study_hours == desired_study_hours:
        target_course = course
        break

# กรณีหาไม่เจอ (fallback) ให้ใช้วิชาแรกสุดที่มี
if target_course is None:
    print(f"⚠️ No course with {desired_study_hours} hours found. Picking the first available course.")
    target_course = list(my_scheduler.courses.values())[0]

target_instructor = my_scheduler.instructors[target_course.instructorId]

print(f"Selected Course: {target_course.course_code} ({target_course.course_name})")
print(f"Requirements: {target_course.study_hours} hours")
print(f"Instructor: {target_instructor.instructorName}")

# 3. Test find_continuous_slots
print("\n--- Testing find_continuous_slots ---")
possible_slots = my_scheduler.find_continuous_slots(
    target_instructor.instructorId, 
    target_course.study_hours,
    target_course.year)

if possible_slots:
    print(f"✅ Found slots: {possible_slots}")
    slot_ids = possible_slots[0]
else:
    print("❌ No continuous slots found.")
    sys.exit()

# 4. Test assign_course
# time_slot=TimeSlot(**time_slot_data)
# slot_ids=time_slots[idx]["SlotID"]
print("\n--- Testing assign_course ---")
my_scheduler.assign_course(target_course, target_instructor, slot_ids)
print(f"Course slots after assign: {target_course.scheduled_slots}")
is_occupied = slot_ids[0] in my_scheduler.student_occ_slots[target_course.year]
print(f"Slot {slot_ids[0]} occupied status (Year {target_course.year}): {is_occupied}")

# 5. Test unassign_course
print("\n--- Testing unassign_course ---")
my_scheduler.unassign_course(target_course, target_instructor, slot_ids)
print(f"Course slots after unassign: {target_course.scheduled_slots}")
is_occupied = slot_ids[0] in my_scheduler.student_occ_slots[target_course.year]
print(f"Slot {slot_ids[0]} occupied status (Year {target_course.year}): {is_occupied}")

# (โค้ดส่วน 1-5 ... เหมือนเดิม ...)

# 6. Test Auto Schedule
print("\n--- Testing auto_schedule ---")
# รีเซ็ตสถานะก่อน
my_scheduler = Scheduler() 
my_scheduler.auto_schedule(use_backtracking=True)

# --- ⭐️ เริ่มแก้ไข/แทนที่ส่วนนับผลรวม (ตั้งแต่บรรทัด 81) ⭐️ ---

# สร้าง Dictionary เพื่อนับ 2 แบบ: ทั้งหมด vs. จัดตารางแล้ว
year_counts_total = {1:0, 2:0, 3:0, 4:0}
total_hours_total = {1:0, 2:0, 3:0, 4:0}
year_counts_scheduled = {1:0, 2:0, 3:0, 4:0}
total_hours_scheduled = {1:0, 2:0, 3:0, 4:0}

scheduled_count = 0
total_count = len(my_scheduler.courses)

for course in my_scheduler.courses.values():
    y = course.year
    h = course.study_hours
    
    # 1. นับยอดรวม "ทั้งหมด" ของปีนั้นๆ
    if y in year_counts_total:
        year_counts_total[y] += 1
        total_hours_total[y] += h

    # 2. นับยอด "ที่จัดตารางสำเร็จ"
    if course.scheduled_slots:
        if y in year_counts_scheduled:
            year_counts_scheduled[y] += 1
            total_hours_scheduled[y] += h
        scheduled_count += 1 # อัปเดตยอดรวมที่จัดได้

print("\n--- Courses per Year and Total Study Hours per Year (Scheduled / Total) ---")
for year in sorted(year_counts_total.keys()):
    # ดึงค่ายอดรวม
    total_c = year_counts_total[year]   
    total_h = total_hours_total[year]   
    
    # ดึงค่ายอดที่จัดได้
    scheduled_c = year_counts_scheduled[year]
    scheduled_h = total_hours_scheduled[year]
    
    # พิมพ์สรุปแยกตามปี
    print(f"  - Year {year}: {scheduled_c}/{total_c} courses, Total {scheduled_h}/{total_h} hours")

# พิมพ์สรุปผลรวมสุดท้าย
print(f"\nAuto-schedule result: {scheduled_count}/{total_count} courses scheduled.")
# --- ⭐️ สิ้นสุดการแก้ไข ⭐️ ---
