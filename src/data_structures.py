# src/data_structures.py

class Course:
    """เก็บข้อมูลรายวิชา"""
    def __init__(self, course_code, course_name, year, credits, study_hours, instructorId, priority):
        self.course_code = course_code
        self.course_name = course_name
        self.year = year
        self.credits = credits
        self.study_hours = study_hours
        self.instructorId = instructorId
        self.priority = priority
        self.scheduled_slots = []  # เก็บช่วงเวลาที่ถูกจัดแล้ว

class Instructor:
    """เก็บข้อมูลอาจารย์"""
    def __init__(self, instructorId, instructorName, department, available_slots, max_weekly_hours, max_daily_courses):
        self.instructorId = instructorId
        self.instructorName = instructorName
        self.department = department
        self.available_slots = available_slots  # list of slot IDs
        self.max_weekly_hours = max_weekly_hours
        self.max_daily_courses = max_daily_courses
        self.assigned_courses = []  # เก็บวิชาที่อาจารย์รับผิดชอบ
        self.assigned_hours = 0     # นับชั่วโมงที่สอนแล้ว

class TimeSlot:
    """เก็บข้อมูลช่วงเวลา"""
    def __init__(self, slot_id, day, time, period, forbidden):
        self.slot_id = slot_id
        self.day = day
        self.time = time
        self.period = period
        self.forbidden = forbidden
        self.is_occupied = False    # ตรวจสอบว่าช่วงเวลานี้ถูกใช้แล้วหรือไม่

class Config:
    """เก็บค่า Config ทั่วไป"""
    def __init__(self, max_weekly_hours, max_daily_courses,max_morning_courses, max_afternoon_courses, lunch_break, forbidden_slot):
        self.max_weekly_hours = max_weekly_hours
        self.max_daily_courses = max_daily_courses
        self.forbidden_slot = forbidden_slot
        self.max_morning_courses = max_morning_courses
        self.max_afternoon_courses = max_afternoon_courses
        self.lunch_break = lunch_break

class Schedule:
    """จัดการตารางเรียนทั้งหมด"""
    def __init__(self):
        self.courses = {}           # {course_code: Course object}
        self.instructors = {}       # {instructorId: Instructor object}
        self.time_slots = {}        # {slot_id: TimeSlot object}
        self.assigned_slots = {}    # {(course_code, slot_id): True} เก็บการจับคู่วิชา-เวลา
        self.config = None          # เพิ่ม attribute สำหรับเก็บ Config object
        
    def add_course(self, **course_data):
        """เพิ่มวิชาลงในระบบ"""
        course = Course(**course_data)
        self.courses[course.course_code] = course
        
    def add_instructor(self, **instructor_data):
        """เพิ่มอาจารย์ลงในระบบ"""
        instructor = Instructor(**instructor_data)
        self.instructors[instructor.instructorId] = instructor
        
    def add_time_slot(self, **time_slot_data):
        """เพิ่มช่วงเวลาลงในระบบ"""
        time_slot = TimeSlot(**time_slot_data)
        self.time_slots[time_slot.slot_id] = time_slot


# src/data_structures.py เพิ่มฟังก์ชันให้ data_structure

# class Course:
#     """เก็บข้อมูลรายวิชา"""
#     def __init__(self, course_code, course_name, year, credits, study_hours, instructorId, priority):
#         self.course_code = course_code
#         self.course_name = course_name
#         self.year = year
#         self.credits = credits
#         self.study_hours = study_hours
#         self.instructorId = instructorId
#         self.priority = priority
#         self.scheduled_slots = []  # เก็บช่วงเวลาที่ถูกจัดแล้ว

# class Instructor:
#     """เก็บข้อมูลอาจารย์"""
#     def __init__(self, instructorId, instructorName, department, available_slots, max_weekly_hours, max_daily_courses):
#         self.instructorId = instructorId
#         self.instructorName = instructorName
#         self.department = department
#         self.available_slots = available_slots  # list of slot IDs
#         self.max_weekly_hours = max_weekly_hours
#         self.max_daily_courses = max_daily_courses
#         self.assigned_courses = []  # เก็บวิชาที่อาจารย์รับผิดชอบ
#         self.assigned_hours = 0     # นับชั่วโมงที่สอนแล้ว

# class TimeSlot:
#     """เก็บข้อมูลช่วงเวลา"""
#     def __init__(self, slot_id, day, time, period, forbidden):
#         self.slot_id = slot_id
#         self.day = day
#         self.time = time
#         self.period = period
#         self.forbidden = forbidden
#         self.is_occupied = False    # ตรวจสอบว่าช่วงเวลานี้ถูกใช้แล้วหรือไม่
#         self.assigned_course = None  # เพิ่มเพื่อเก็บวิชาที่ถูกจัด

# class Schedule:
#     """จัดการตารางเรียนทั้งหมด"""
#     def __init__(self):
#         self.courses = {}           # {course_code: Course object}
#         self.instructors = {}       # {instructorId: Instructor object}
#         self.time_slots = {}        # {slot_id: TimeSlot object}
#         self.assigned_slots = {}    # {(course_code, slot_id): True} เก็บการจับคู่วิชา-เวลา
#         self.year_schedules = {1: {}, 2: {}, 3: {}, 4: {}}  # เพิ่มสำหรับเก็บตารางตามปี
        
#     def add_course(self, course_data):
#         """เพิ่มวิชาลงในระบบ"""
#         course = Course(**course_data)
#         self.courses[course.course_code] = course
        
#     def add_instructor(self, instructor_data):
#         """เพิ่มอาจารย์ลงในระบบ"""
#         instructor = Instructor(**instructor_data)
#         self.instructors[instructor.instructorId] = instructor
        
#     def add_time_slot(self, time_slot_data):
#         """เพิ่มช่วงเวลาลงในระบบ"""
#         time_slot = TimeSlot(**time_slot_data)
#         self.time_slots[time_slot.slot_id] = time_slot

#     def assign_course_to_slot(self, course_code, slot_id):
#         """กำหนดวิชาให้กับช่วงเวลา"""
#         if course_code in self.courses and slot_id in self.time_slots:
#             course = self.courses[course_code]
#             time_slot = self.time_slots[slot_id]

#             # ตรวจสอบว่าช่วงเวลาว่าง
#             if not time_slot.is_occupied:
#                 time_slot.is_occupied = True
#                 time_slot.assigned_course = course_code

#                 course.scheduled_slots.append(slot_id)

#                 # อัพเดตข้อมูลอาจารย์
#                 instructor = self.instructors[course.instructorId]
#                 instructor.assigned_hours += 1
#                 if course_code not in instructor.assigned_courses:
#                     instructor.assigned_courses.append(course_code)

#                 # บันทึกการจับคู่
#                 self.assigned_slots[(course_code, slot_id)] = True

#                 # อัพเดตตารางตามปี
#                 year = course.year
#                 if time_slot.day not in self.year_schedules[year]:
#                     self.year_schedules[year][time_slot.day] = {}
#                 self.year_schedules[year][time_slot.day][time_slot.time] = {
#                     'course': course_code,
#                     'instructor': course.instructorId
#                 }

#                 return True
#         return False

#     def get_course_at_timeslot(self, year, day, time):
#         """หาวิชาที่ปีนั้นเรียนในวันและเวลาที่กำหนด"""
#         if day in self.year_schedules[year] and time in self.year_schedules[year][day]:
#             return self.year_schedules[year][day][time]
#         return None

#     # หรือถ้าอยากใช้วิธีแบบง่ายๆ ให้ใช้ฟังก์ชันนี้แทน
#     def find_course_at_timeslot(self, year, day, time):
#         """หาวิชาที่ปีนั้นเรียนในวันและเวลาที่กำหนด (แบบค้นหาทั้งหมด)"""
#         for course in self.courses.values():
#             if course.year != year:
#                 continue
                
#             for slot_id in course.scheduled_slots:
#                 slot = self.time_slots[slot_id]
#                 if slot.day == day and slot.time == time:
#                     return {
#                         'course': course.course_code,
#                         'instructor': course.instructorId
#                     }
#         return None