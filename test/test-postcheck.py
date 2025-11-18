# tests/test_validate_post_schedule_real.py
import os
import pytest
from input_handler import load_data
from validator import validate_post_schedule

@pytest.fixture
def real_schedule():
    """โหลด Schedule จาก data.json จริง"""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "data.json")
    schedule = load_data(data_path)
    return schedule

@pytest.fixture
def timetable_and_time_slots(real_schedule):
    """
    สร้าง timetable (day -> list of cells) และ time_slots list
    format ของ cell: "COURSE_CODE (InstructorName)" หรือ None / "Lunch Break"
    """
    timetable = {}
    time_slots_list = []

    for day in ['Monday','Tuesday','Wednesday','Thursday','Friday']:
        timetable[day] = []

    for slot in real_schedule.time_slots.values():
        # เตรียม time_slots list
        time_slots_list.append({
            "slotId": slot.slotId,
            "day": slot.day,
            "period": slot.period,
            "forbidden": getattr(slot, "forbidden", False)
        })

        # หา course ใน slot นี้
        cell_value = None
        for course in real_schedule.courses.values():
            if slot.slotId in course.scheduled_slots:
                instructor_name = real_schedule.instructors[course.instructorId].instructorName
                cell_value = f"{course.course_code} ({instructor_name})"
                break

        # ถ้าเป็นช่วง lunch
        if slot.time == real_schedule.config.lunch_break:
            cell_value = "Lunch Break"

        timetable[slot.day].append(cell_value)

    return timetable, time_slots_list

def test_post_schedule_validation(real_schedule, timetable_and_time_slots):
    timetable, time_slots_list = timetable_and_time_slots

    # ดึง instructors และ config
    instructors = {iid: {"instructorName": ins.instructorName} for iid, ins in real_schedule.instructors.items()}
    config_dict = real_schedule.config.__dict__

    # เรียก validate_post_schedule
    valid, msg = validate_post_schedule(timetable, instructors, time_slots_list, config_dict)

    # ตรวจสอบว่าผ่าน validation
    assert valid, f"Post-schedule validation failed: {msg}"
