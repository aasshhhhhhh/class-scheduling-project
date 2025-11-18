import sys
import os

# เพิ่ม path เพื่อ import จากโฟลเดอร์เดียวกัน
sys.path.append(os.path.dirname(__file__))

from input_handler import load_data
from constraints.precheck import check_assign_rules

class Scheduler:
    def __init__(self, schedule=None):
        """
        Initialize Scheduler with Schedule object
        """
        if schedule is None:
            # โหลดข้อมูลอัตโนมัติถ้าไม่ได้ส่ง Schedule object มา
            data_path = os.path.join(os.path.dirname(__file__), "..", "data", "data.json")
            schedule = load_data(data_path)
        
        self.schedule = schedule
        self.courses = schedule.courses
        self.instructors = schedule.instructors
        self.time_slots = schedule.time_slots

        # แยกวิชาตามชั้นปี
        self.courses_by_year = {1: [], 2: [], 3: [], 4: []}
        for course in self.courses.values():
            self.courses_by_year[course.year].append(course)

        self.student_occ_slots = {1: set(), 2: set(), 3: set(), 4: set()} # เก็บ slot_id ที่ไม่ว่างสำหรับปีนั้นๆ
        self.instructor_occ_slots = {i_id: set() for i_id in self.instructors} # เก็บ slot_id ที่อาจารย์แต่ละคนไม่ว่าง

    def find_continuous_slots(self, instructor_id, study_hours, student_year):

        instructor = self.instructors.get(instructor_id)
        if not instructor:
            return []
        
        student_busy = self.student_occ_slots[student_year]
        instructor_busy = self.instructor_occ_slots[instructor_id]
    
        day_slots = {}
        for sid, slot in self.time_slots.items():
            if slot.time == "12:30-13:30" or slot.forbidden:
                continue

            if sid in student_busy or sid in instructor_busy:
                continue

            if sid not in instructor.available_slots:
                continue

            if slot.day not in day_slots:
                day_slots[slot.day] = []
            day_slots[slot.day].append(slot)

        for day in day_slots:
            day_slots[day].sort(key=lambda s: s.period)

        possible_groups = []
        for day in sorted(day_slots.keys()):
            slots = day_slots[day]
            for i in range(len(slots) - study_hours + 1):
                group = slots[i:i + study_hours]
                slot_ids = [s.slot_id for s in group]
                # ตรวจสอบว่า slot_id ต่อเนื่องกัน
                if all(slot_ids[j+1] - slot_ids[j] == 1 for j in range(len(slot_ids)-1)):
                    possible_groups.append(slot_ids)
        
        return possible_groups

    def assign_course(self, course, instructor, slot_ids):
        # จองเวลาให้นศ.
        for sid in slot_ids:
            self.student_occ_slots[course.year].add(sid)
            self.instructor_occ_slots[instructor.instructorId].add(sid)
            # Update objects
            course.scheduled_slots.append(sid)

        instructor.assigned_courses.append(course)
        instructor.assigned_hours += course.study_hours

        # Update year_schedule structure for precheck
        for sid in slot_ids:
            slot = self.time_slots[sid]
            if slot.day not in self.schedule.year_schedules[course.year]:
                self.schedule.year_schedules[course.year][slot.day] = {}
            self.schedule.year_schedules[course.year][slot.day][slot.time] = f"{course.course_code}"

    def unassign_course(self, course, instructor, slot_ids):
        for sid in slot_ids:
            self.student_occ_slots[course.year].remove(sid)
            self.instructor_occ_slots[instructor.instructorId].remove(sid)
            course.scheduled_slots.remove(sid)
            
            slot = self.time_slots[sid]
            if (slot.day in self.schedule.year_schedules[course.year] and 
                slot.time in self.schedule.year_schedules[course.year][slot.day]):
                del self.schedule.year_schedules[course.year][slot.day][slot.time]

        if course.course_code in instructor.assigned_courses:
            instructor.assigned_courses.remove(course)

        instructor.assigned_hours -= course.study_hours

    def schedule_backtrack(self,year, courses_list, sorted_courses):
        if courses_list >= len(sorted_courses):
            return True
        
        course = sorted_courses[courses_list]
        instructor = self.instructors[course.instructorId]

        possible_slots_groups = self.find_continuous_slots(instructor.instructorId, course.study_hours, year)
        # Call the new precheck function (from constraint/precheck.py)
        for slot_ids in possible_slots_groups:
            is_valid = check_assign_rules(
                instructor, 
                course, 
                slot_ids, 
                self.time_slots, 
                self.schedule.year_schedules[course.year], # Get the specific year's schedule
                self.schedule.config
        )
        
        if is_valid:
                self.assign_course(course, instructor, slot_ids)
                # Recursive ไปวิชาถัดไป
                if self.schedule_recursive(year, courses_list + 1, sorted_courses):
                    return True
                
                # Backtrack: ถ้าย้อนกลับมาแปลว่าทางตัน ให้ยกเลิกการจองนี้
                self.unassign_course(course, instructor, slot_ids)
        
        # ถ้าวนลูปทุก slot แล้วยังลงไม่ได้ แสดงว่า path นี้ล้มเหลว
        return False
        
    # Schedule using greedy algorithm
    def auto_schedule(self, use_backtracking=True):
        for course in self.courses.values():
            self.courses_by_year[course.year].append(course)

        for year in range(1, 5):
            print(f"\n=== Scheduling Year {year} ===")
            current_year_courses = sorted(
                self.courses_by_year[year], 
                key=lambda c: (c.priority, -c.study_hours, c.course_code)
            )

            success = self.schedule_recursive(year, 0, current_year_courses)
            if success:
                print(f"✅ Year {year} scheduling complete.")
            else:
                print(f"❌ Failed to schedule Year {year}. Needs manual adjustment.")

    def schedule_recursive(self, year, course_idx, courses_list):
        # Base Case: ถ้าจัดครบทุกวิชาในรายการแล้ว แสดงว่าสำเร็จ
        if course_idx >= len(courses_list):
            return True
        
        course = courses_list[course_idx]
        instructor = self.instructors[course.instructorId]

        possible_slot_groups = self.find_continuous_slots(instructor.instructorId, course.study_hours, year)

        # 2. ลองวางทีละความเป็นไปได้
        for slot_ids in possible_slot_groups:
            
            is_valid = check_assign_rules(
                instructor,
                course,
                slot_ids,
                self.time_slots,
                self.schedule.year_schedules[year], # ส่งตารางเรียนของปีปัจจุบันไปเช็ค
                self.schedule.config
            )

            if is_valid:
                # --- Action: ---
                self.assign_course(course, instructor, slot_ids)

                # --- Recursive:  ---
                if self.schedule_recursive(year, course_idx + 1, courses_list):
                    return True # ถ้าวิชาถัดๆ ไปจัดลงตัวหมด ให้ return True กลับมา

                # --- Backtrack: ถ้าไปต่อไม่ได้(ยกเลิกการจอง) ---
                self.unassign_course(course, instructor, slot_ids)

        return False
           