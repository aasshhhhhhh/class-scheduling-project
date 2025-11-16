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

class Schedule:
    """จัดการตารางเรียนทั้งหมด"""
    def __init__(self):
        self.courses = {}           # {course_code: Course object}
        self.instructors = {}       # {instructorId: Instructor object}
        self.time_slots = {}        # {slot_id: TimeSlot object}
        self.assigned_slots = {}    # {(course_code, slot_id): True} เก็บการจับคู่วิชา-เวลา
        
    def add_course(self, course_data):
        """เพิ่มวิชาลงในระบบ"""
        course = Course(**course_data)
        self.courses[course.course_code] = course
        
    def add_instructor(self, instructor_data):
        """เพิ่มอาจารย์ลงในระบบ"""
        instructor = Instructor(**instructor_data)
        self.instructors[instructor.instructorId] = instructor
        
    def add_time_slot(self, time_slot_data):
        """เพิ่มช่วงเวลาลงในระบบ"""
        time_slot = TimeSlot(**time_slot_data)
        self.time_slots[time_slot.slot_id] = time_slot