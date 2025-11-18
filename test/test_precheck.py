import sys
import os
# โค้ดนี้จะย้อนกลับไป 2 ระดับชั้น (จาก test/ ไป project root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# บรรทัด import ต้องอยู่หลังจากโค้ดข้างบน
from constraints.precheck import check_assign_rules

import unittest
from unittest.mock import MagicMock
# Import the function to be tested
from constraints.precheck import check_assign_rules

# --- Mock Data Structures (เพื่อจำลอง Data Structure ที่จำเป็น) ---
# เราจะสร้าง Mock Class ที่มีคุณสมบัติที่จำเป็นต่อการทดสอบเท่านั้น
# ข้อมูลเหล่านี้จำลองมาจาก data_structures.py

class MockConfig:
    def __init__(self, max_morning_courses, max_afternoon_courses):
        self.max_morning_courses = max_morning_courses
        self.max_afternoon_courses = max_afternoon_courses

class MockCourse:
    def __init__(self, course_code, study_hours, scheduled_slots=None):
        self.course_code = course_code
        self.study_hours = study_hours
        self.scheduled_slots = scheduled_slots if scheduled_slots is not None else []

class MockInstructor:
    def __init__(self, max_weekly_hours, max_daily_courses, assigned_hours, assigned_courses):
        self.max_weekly_hours = max_weekly_hours
        self.max_daily_courses = max_daily_courses
        self.assigned_hours = assigned_hours
        self.assigned_courses = assigned_courses # list of MockCourse objects

class MockTimeSlot:
    def __init__(self, slot_id, day, time, period):
        self.slot_id = slot_id
        self.day = day
        self.time = time
        self.period = period

# --- Test Class ---

class TestCheckAssignRules(unittest.TestCase):

    def setUp(self):
        # ตั้งค่า Mock Config ทั่วไป
        self.config = MockConfig(
            max_morning_courses=2,
            max_afternoon_courses=2
        )

        # ตั้งค่า TimeSlot Map
        self.time_slots_map = {
            1: MockTimeSlot(1, "Mon", "08:30-09:30", "morning"),
            2: MockTimeSlot(2, "Mon", "09:30-10:30", "morning"),
            3: MockTimeSlot(3, "Mon", "10:30-11:30", "morning"),
            4: MockTimeSlot(4, "Mon", "13:30-14:30", "afternoon"),
            5: MockTimeSlot(5, "Tue", "08:30-09:30", "morning"),
            6: MockTimeSlot(6, "Tue", "13:30-14:30", "afternoon"),
        }

    # 1. Test Max Weekly Hours
    def test_max_weekly_hours_exceeded(self):
        """Should fail if assigned_hours + course.study_hours > max_weekly_hours"""
        # อาจารย์สอนได้สูงสุด 10 ชั่วโมง/สัปดาห์, สอนไปแล้ว 8 ชั่วโมง
        instructor = MockInstructor(
            max_weekly_hours=10,
            max_daily_courses=3,
            assigned_hours=8,
            assigned_courses=[]
        )
        # วิชาใหม่ 3 ชั่วโมง
        course = MockCourse(course_code="NEW300", study_hours=3)
        slot_ids = [5, 6] # ไม่สำคัญสำหรับเทสนี้ แต่ต้องใส่
        
        # 8 + 3 = 11 > 10 --> Should FAIL (return False)
        result = check_assign_rules(
            instructor, course, slot_ids, self.time_slots_map, {}, self.config
        )
        self.assertFalse(result, "Test failed: Max weekly hours exceeded but check passed.")

    def test_max_weekly_hours_allowed(self):
        """Should pass if assigned_hours + course.study_hours <= max_weekly_hours"""
        instructor = MockInstructor(
            max_weekly_hours=10,
            max_daily_courses=3,
            assigned_hours=8,
            assigned_courses=[]
        )
        course = MockCourse(course_code="NEW100", study_hours=2)
        slot_ids = [5, 6]
        
        # 8 + 2 = 10 <= 10 --> Should PASS (return True)
        result = check_assign_rules(
            instructor, course, slot_ids, self.time_slots_map, {}, self.config
        )
        # ในความเป็นจริงผลลัพธ์จะเป็น False เพราะต้องผ่านเงื่อนไขอื่นๆ ด้วย
        # แต่เพื่อ isolate test (สมมติว่าเงื่อนไขอื่นผ่านหมด) เราจะเช็คแค่ Logic ที่เกี่ยวข้อง
        # เนื่องจากฟังก์ชันนี้เช็คทั้งหมด เราคาดหวังว่าเงื่อนไขนี้ 'ไม่' ทำให้เกิด False
        self.assertTrue(result, "Test failed: Max weekly hours within limit but check failed.")


    # 2. Test Max Daily Courses
    def test_max_daily_courses_exceeded(self):
        """Should fail if assigning course exceeds max_daily_courses on the same day"""
        # อาจารย์สอนได้สูงสุด 2 วิชา/วัน
        course_A = MockCourse(course_code="INS100", study_hours=1, scheduled_slots=[5]) # สอนวันอังคาร
        course_B = MockCourse(course_code="INS200", study_hours=1, scheduled_slots=[6]) # สอนวันอังคาร
        
        instructor = MockInstructor(
            max_weekly_hours=10,
            max_daily_courses=2,
            assigned_hours=2,
            assigned_courses=[course_A, course_B] # สอนไปแล้ว 2 วิชาในวันอังคาร
        )
        # วิชาใหม่
        course_new = MockCourse(course_code="NEW300", study_hours=1)
        # พยายามจัดลงวันอังคาร (slot_id=5, 6)
        slot_ids = [5] # Slot วันอังคาร
        
        # 2 + 1 = 3 > 2 --> Should FAIL
        result = check_assign_rules(
            instructor, course_new, slot_ids, self.time_slots_map, {}, self.config
        )
        self.assertFalse(result, "Test failed: Max daily courses exceeded but check passed.")

    def test_max_daily_courses_allowed(self):
        """Should pass if assigning course is within max_daily_courses"""
        # อาจารย์สอนได้สูงสุด 2 วิชา/วัน
        course_A = MockCourse(course_code="INS100", study_hours=1, scheduled_slots=[5]) # สอนวันอังคาร
        
        instructor = MockInstructor(
            max_weekly_hours=10,
            max_daily_courses=2,
            assigned_hours=1,
            assigned_courses=[course_A] # สอนไปแล้ว 1 วิชาในวันอังคาร
        )
        # วิชาใหม่
        course_new = MockCourse(course_code="NEW200", study_hours=1)
        # พยายามจัดลงวันอังคาร (slot_id=6)
        slot_ids = [6] # Slot วันอังคาร
        
        # 1 + 1 = 2 <= 2 --> Should PASS (แต่ต้องผ่านเงื่อนไขอื่นด้วย)
        result = check_assign_rules(
            instructor, course_new, slot_ids, self.time_slots_map, {}, self.config
        )
        self.assertTrue(result, "Test failed: Max daily courses within limit but check failed.")

    # 3. Test Max Morning/Afternoon Courses
    def test_max_morning_courses_exceeded(self):
        """Should fail if assigning course exceeds max_morning_courses for the year schedule"""
        # Config: สอนเช้าสูงสุด 2 วิชา
        # Year Schedule: วันจันทร์มีวิชา "Y1M1" และ "Y1M2" ในช่วงเช้าแล้ว (2 วิชา)
        year_schedule = {
            "Mon": {
                "08:30-09:30": "Y1M1", # slot 1
                "09:30-10:30": "Y1M2"  # slot 2
            }
        }
        # อาจารย์และวิชาที่จะจัดใหม่
        instructor = MockInstructor(max_weekly_hours=10, max_daily_courses=3, assigned_hours=0, assigned_courses=[])
        course_new = MockCourse(course_code="Y1M3", study_hours=1)
        # พยายามจัดลง slot 3 (วันจันทร์, ช่วงเช้า)
        slot_ids = [3]
        
        # 2 + 1 = 3 > 2 --> Should FAIL
        result = check_assign_rules(
            instructor, course_new, slot_ids, self.time_slots_map, year_schedule, self.config
        )
        self.assertFalse(result, "Test failed: Max morning courses exceeded but check passed.")

    def test_max_afternoon_courses_allowed(self):
        """Should pass if assigning course is within max_afternoon_courses for the year schedule"""
        # Config: สอนบ่ายสูงสุด 2 วิชา
        # Year Schedule: วันจันทร์มีวิชา "Y1A1" ในช่วงบ่ายแล้ว (1 วิชา)
        year_schedule = {
            "Mon": {
                "13:30-14:30": "Y1A1", # slot 4
            }
        }
        # อาจารย์และวิชาที่จะจัดใหม่
        instructor = MockInstructor(max_weekly_hours=10, max_daily_courses=3, assigned_hours=0, assigned_courses=[])
        course_new = MockCourse(course_code="Y1A2", study_hours=1)
        # พยายามจัดลง slot 4 (วันจันทร์, ช่วงบ่าย)
        slot_ids = [4]
        
        # 1 + 1 = 2 <= 2 --> Should PASS (ถ้าเงื่อนไขอื่นผ่านหมด)
        # Note: การวางวิชาใหม่ทับ slot 4 ใน year_schedule จะเป็นการชนตาราง ซึ่งฟังก์ชันนี้ไม่ได้เช็ค
        # แต่เพื่อการทดสอบเงื่อนไข morning/afternoon โดยเฉพาะ เราจะสมมติว่า slot นั้นว่าง
        # (เพราะ check_assign_rules ถูกเรียก *หลัง* find_continuous_slots)
        
        # แก้ไข: เนื่องจาก check_assign_rules นับ course_code จาก year_schedule ก่อน แล้วค่อยเพิ่มวิชาใหม่
        # ถ้า course_new ถูกวางใน slot เดียวกับ Y1A1, มันจะนับ Y1A1 (จาก year_schedule) และ Y1A2 (วิชาใหม่)
        # ถ้า course_new ถูกวางใน slot ใหม่ slot_ids = [new_slot_id_after_4]
        
        # สร้าง MockTimeSlot ใหม่สำหรับเทสนี้เพื่อให้ slot_ids ไม่ซ้ำและอยู่ในช่วงบ่าย
        self.time_slots_map[7] = MockTimeSlot(7, "Mon", "14:30-15:30", "afternoon")
        slot_ids = [7] # slot ใหม่วันจันทร์บ่าย
        
        # นับ: "Y1A1" (1) + "Y1A2" (1) = 2 <= 2 --> Should PASS
        result = check_assign_rules(
            instructor, course_new, slot_ids, self.time_slots_map, year_schedule, self.config
        )
        self.assertTrue(result, "Test failed: Max afternoon courses within limit but check failed.")
        
    def test_reassigning_same_course_on_same_day(self):
        """Should fail if a course is already assigned to the same instructor on the same day (to prevent double counting)"""
        # อาจารย์สอนได้สูงสุด 3 วิชา/วัน
        course_A = MockCourse(course_code="INS100", study_hours=1, scheduled_slots=[5]) # สอนวันอังคาร
        
        instructor = MockInstructor(
            max_weekly_hours=10,
            max_daily_courses=3,
            assigned_hours=1,
            assigned_courses=[course_A] # สอนไปแล้ว 1 วิชาในวันอังคาร
        )
        # พยายามจัด course_A ซ้ำใน slot วันอังคาร
        course_to_reassign = course_A
        slot_ids = [6] # Slot วันอังคาร
        
        # courses_on_day_set จะมี {'INS100'} อยู่แล้ว
        # ถ้า course_to_reassign.course_code ('INS100') อยู่ใน set นี้ --> Should FAIL
        result = check_assign_rules(
            instructor, course_to_reassign, slot_ids, self.time_slots_map, {}, self.config
        )
        self.assertFalse(result, "Test failed: Reassigning same course on same day passed.")


if __name__ == '__main__':
    # สำหรับการรันเทสจาก command line
    # (สมมติว่าไฟล์อยู่ในโครงสร้าง /project/constraints/precheck.py และเทสอยู่ใน /project/tests/test_precheck.py)
    # เราต้องมั่นใจว่า Python สามารถ import constraints.precheck ได้
    # หากรันจาก command line ใน directory ที่ถูกต้อง
    # ให้ใช้คำสั่ง: python -m unittest test_precheck.py
    unittest.main(argv=['first-arg-is-ignored'], exit=False)