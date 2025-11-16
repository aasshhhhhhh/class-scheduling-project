import sys
import os

# เพิ่ม path เพื่อ import จากโฟลเดอร์เดียวกัน
sys.path.append(os.path.dirname(__file__))

from input_handler import load_data

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

    def find_continuous_slots(self, instructor_id, study_hours):

        instructor = self.instructors.get(instructor_id)
        if not instructor:
            return []
    
        day_slots = {}
        for sid in instructor.available_slots:
            slot = self.time_slots[sid]
            if slot.is_occupied or slot.forbidden:
                continue
            if sid in [5,6,7,8]:
                continue
            if slot.day not in day_slots:
                day_slots[slot.day] = []
            day_slots[slot.day].append(slot)
        for day in day_slots:
            day_slots[day].sort(key=lambda s: s.period)


        for day in sorted(day_slots.keys()):
            slots = day_slots[day]
            for i in range(len(slots) - study_hours + 1):
                group = slots[i:i + study_hours]
                slot_ids = [s.slot_id for s in group]
            # ตรวจสอบว่า slot_id ต่อเนื่องกัน
            if all(slot_ids[j+1] - slot_ids[j] == 1 for j in range(len(slot_ids)-1)):
                return slot_ids
            
        return [] 

    
    def can_assign(self, instructor, course, slot_ids):
        if instructor.assigned_hours + course.study_hours > instructor.max_weekly_hours:
            return False

        daily_count = {}
        for cid in instructor.assigned_courses:
            c = self.courses[cid]
            for sid in c.scheduled_slots:
                day = self.time_slots[sid].day
                if day not in daily_count:
                    daily_count[day] = 0
                daily_count[day] += 1

        #loop slot ใหม่ ที่เราจะลองจัดวิชา
        for sid in slot_ids:
            day = self.time_slots[sid].day
            if daily_count.get(day, 0) + 1 > instructor.max_daily_courses:
                return False

        return True

    def assign_course(self, course, instructor, slot_ids):
        for sid in slot_ids:
            self.time_slots[sid].is_occupied = True
            course.scheduled_slots.append(sid)
        instructor.assigned_courses.append(course.course_code)
        instructor.assigned_hours += course.study_hours

    def unassign_course(self, course, instructor, slot_ids):
        for sid in slot_ids:
            self.time_slots[sid].is_occupied = False
            if sid in course.scheduled_slots:
                course.scheduled_slots.remove(sid)
        if course.course_code in instructor.assigned_courses:
            instructor.assigned_courses.remove(course.course_code)
        instructor.assigned_hours -= course.study_hours

    def schedule_backtrack(self, courses_list):
        if not courses_list:
            return True
        course = courses_list[0]
        instructor = self.instructors[course.instructorId]
        slot_ids = self.find_continuous_slots(instructor, course.study_hours)

      
        if slot_ids and self.can_assign(instructor, course, slot_ids):
            self.assign_course(course, instructor, slot_ids)
            if self.schedule_backtrack(courses_list[1:]):
                return True
            self.unassign_course(course, instructor, slot_ids)

        #ตัวแปร remaining_courses เป็น list ของวิชาที่เหลือ ยกเว้นตัวแรก
        remaining_courses = courses_list[1:]
        return self.schedule_backtrack(remaining_courses)
        

    #จัดตารางแบบ greedy
    def auto_schedule(self, use_backtracking=True):
        sorted_courses = sorted(self.courses.values(), key=lambda c: c.priority, reverse=True)
        #สร้างลิสต์เก็บวิชาที่ยังจัดไม่ได้จากขั้นตอนแรกเพื่อจะเอาไปให้ backtracking ลองจัดต่อ
        unscheduled = []

        for course in sorted_courses:
            instructor = self.instructors[course.instructorId]
            slot_ids = self.find_continuous_slots(instructor, course.study_hours)

            #ถ้าพบ slot_ids และ can_assign คืน True
            if slot_ids and self.can_assign(instructor, course, slot_ids):
                self.assign_course(course, instructor, slot_ids)
            else:
                unscheduled.append(course)

        if unscheduled and use_backtracking:
            success = self.schedule_backtrack(unscheduled)
            if success:
                print("Backtracking succeeded.")
            else:
                print("Backtracking failed for some courses.")


scheduler = Scheduler()
slot = scheduler.find_continuous_slots(instructor_id="INT01",study_hours=3)
print(slot)