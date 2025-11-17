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
        # แบ่ง courses ตามปี
        self.courses_by_year = {1: [], 2: [], 3: [], 4: []}
        for course in self.courses:
            self.courses_by_year[course["year"]].append(course)

        # *** ส่วนที่เพิ่ม: เก็บ assigned slots ของอาจารย์ทั้งหมด ***
        self.instructor_assigned_slots = {i["instructorId"]: set() for i in data["instructors"]}



    def find_continuous_slots(self, course, instructor, assigned_slots_year):
        # รวม slots ที่ถูกจองไปแล้วทั้งหมดสำหรับอาจารย์คนนี้ (จากชั้นปีอื่นๆ)
        # และ slots ที่ถูกจองไปแล้วในชั้นปีนี้ (assigned_slots_year)
        all_assigned_slots_for_instructor = assigned_slots_year.union(
            self.instructor_assigned_slots.get(instructor["instructorId"], set())
        )

        available = [sid for sid in instructor["available_slots"]
                     # ตรวจสอบว่า slot ไม่ถูกจองไปแล้ว และไม่เป็น forbidden
                     if sid not in all_assigned_slots_for_instructor
                     and not self.time_slots[sid]["forbidden"]]

        #print("Instructor:", instructor["instructorId"])
        #print("Available slots (filtered):", available)

        available.sort(key=lambda sid: (self.time_slots[sid]["day"], self.time_slots[sid]["time"]))

        for i in range(len(available) - course["study_hours"] + 1):
            group = available[i:i + course["study_hours"]]
            consecutive = True
            for j in range(1, len(group)):
                # ต้องเป็นวันเดียวกันและเวลาต่อกัน (สมมติว่า slot ID เรียงเวลาอยู่แล้ว)
                if self.time_slots[group[j]]["day"] != self.time_slots[group[j-1]]["day"]:
                    consecutive = False
                    break
            if consecutive:
                return group
        return None

    # wrapper สำหรับใช้งานด้วย instructor_id + study_hours
    def find_continuous_slots_by_id(self, instructor_id, study_hours, assigned_slots_year=None):
        if assigned_slots_year is None:
            assigned_slots_year = set()
        instructor = self.instructors[instructor_id]
        course = {"study_hours": study_hours}
        # ฟังก์ชันนี้ใช้ slots ที่ถูกจองทั้งหมดของอาจารย์ (จาก self.instructor_assigned_slots)
        # และรวม assigned_slots_year ที่ส่งเข้ามา (ถ้ามี)
        return self.find_continuous_slots(course, instructor, assigned_slots_year)

    def schedule_year(self, year):
        print(f"\n=== Year {year} ===")
        assigned_slots_year = set()
        
        # เรียงตาม: 1. study_hours 2. priority 3. course_code 
        
        sorted_courses = sorted(self.courses_by_year[year], 
        key=lambda c: (-c["study_hours"], c["priority"], c["course_code"]))
        
        for course in sorted_courses:
            instructor = self.instructors[course["instructorId"]]
            slots = self.find_continuous_slots(course, instructor, assigned_slots_year)
            
            if slots and len(slots) == course["study_hours"]:
                for sid in slots:
                    assigned_slots_year.add(sid)
                    
                # อัปเดต assigned slots ของอาจารย์คนนี้ในระดับรวม
                self.instructor_assigned_slots[instructor["instructorId"]].update(slots) 
                
                print(f'{course["course_code"]} assigned slots: {slots}')
            else:
                print(f'{course["course_code"]} could NOT be fully assigned! ({course["study_hours"]} hours)')
                if slots is None and course["study_hours"] > 1:
                    print("  Reason: Not enough continuous slots found.")

    def schedule_all(self):
        for year in range(1, 5):
            self.schedule_year(year)