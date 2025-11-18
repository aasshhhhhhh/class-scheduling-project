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

# 6. Test Auto Schedule
print("\n--- Testing auto_schedule ---")
# รีเซ็ตสถานะก่อน
my_scheduler = Scheduler() 
my_scheduler.auto_schedule(use_backtracking=True)

# นับจำนวนวิชาที่ลงทะเบียนสำเร็จ
scheduled_count = sum(1 for c in my_scheduler.courses.values() if c.scheduled_slots)
total_count = len(my_scheduler.courses)
print(f"Auto-schedule result: {scheduled_count}/{total_count} courses scheduled.")