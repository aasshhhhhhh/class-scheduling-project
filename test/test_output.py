# src/test_output.py
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from data_structures import Course, Instructor, TimeSlot, Schedule
from output_formatter import OutputFormatter

def test_output_formatter():
    """ทดสอบ Output Formatter ของคุณ"""
    print("🧪 ทดสอบ Output Formatter...")
    
    # สร้างข้อมูลทดสอบ
    schedule = Schedule()
    
    # เพิ่มอาจารย์
    schedule.instructors["INT01"] = Instructor(
        instructorId="INT01",
        instructorName="ดร.สมชาย",
        department="ENE", 
        available_slots=[1,2,3],
        max_weekly_hours=15,
        max_daily_courses=2
    )
    
    schedule.instructors["INT02"] = Instructor(
        instructorId="INT02", 
        instructorName="ดร.อนิกา",
        department="MTH",
        available_slots=[4,5,6],
        max_weekly_hours=15,
        max_daily_courses=2
    )
    
    # เพิ่มวิชา
    schedule.courses["TEST101"] = Course(
        course_code="TEST101",
        course_name="วิชาทดสอบวิศวกรรม",
        year=1,
        credits=3,
        study_hours=3,
        instructorId="INT01",
        priority=1
    )
    
    schedule.courses["TEST102"] = Course(
        course_code="TEST102",
        course_name="วิชาทดสอบคณิตศาสตร์", 
        year=1,
        credits=2,
        study_hours=2,
        instructorId="INT02",
        priority=1
    )
    
    # เพิ่มช่วงเวลา
    time_slots_data = [
        (1, "Monday", "08:30-09:30", "morning", False),
        (2, "Monday", "09:30-10:30", "morning", False),
        (3, "Monday", "10:30-11:30", "morning", False),
        (4, "Tuesday", "08:30-09:30", "morning", False),
        (5, "Tuesday", "09:30-10:30", "morning", False),
    ]
    
    for slot_data in time_slots_data:
        schedule.time_slots[slot_data[0]] = TimeSlot(*slot_data)
    
    # จัดวิชา (จำลอง)
    schedule.courses["TEST101"].scheduled_slots = [1, 2, 3]
    schedule.courses["TEST102"].scheduled_slots = [4, 5]
    
    schedule.instructors["INT01"].assigned_hours = 3
    schedule.instructors["INT01"].assigned_courses = ["TEST101"]
    
    schedule.instructors["INT02"].assigned_hours = 2  
    schedule.instructors["INT02"].assigned_courses = ["TEST102"]
    
    for slot_id in [1, 2, 3, 4, 5]:
        schedule.time_slots[slot_id].is_occupied = True
    
    # ทดสอบ Output Formatter
    formatter = OutputFormatter(schedule)
    
    print("\n" + "="*50)
    print("📊 ทดสอบ display_summary():")
    formatter.display_summary()
    
    print("\n" + "="*50)
    print("🎓 ทดสอบ display_schedule_by_year(1):")
    formatter.display_schedule_by_year(1)
    
    # print("\n" + "="*50) 
    # print("👨‍🏫 ทดสอบ display_instructor_schedule('INT01'):")
    # formatter.display_instructor_schedule("INT01")
    
    # print("\n" + "="*50)
    # print("👨‍🏫 ทดสอบ display_instructor_schedule('INT02'):")
    # formatter.display_instructor_schedule("INT02")
    
    print("\n✅ การทดสอบเสร็จสิ้น!")

if __name__ == "__main__":
    test_output_formatter()