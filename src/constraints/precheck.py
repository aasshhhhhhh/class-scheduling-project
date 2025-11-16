# File: precheck.py

def check_assign_rules(instructor, course, slot_ids, time_slots_map, year_schedule, config):

    """ Checks logic-based constraints *after* finding available slots. """
    
    # --- 1. Check Max Weekly Hours (from scheduler.can_assign) ---
    if instructor.assigned_hours + course.study_hours > instructor.max_weekly_hours:
        return False

    slot_day = time_slots_map[slot_ids[0]].day
    
    # --- 2. Check Max Daily Courses ---
    
    # Find courses already assigned to this instructor on this day
    courses_on_day_set = set()
    for c in instructor.assigned_courses:
        if c.scheduled_slots: # Check if course is actually scheduled
            day_of_course = time_slots_map[c.scheduled_slots[0]].day
            if day_of_course == slot_day:
                courses_on_day_set.add(c.course_code)
    
    # Check if this new course exceeds the limit
    if course.course_code not in courses_on_day_set:
        if len(courses_on_day_set) + 1 > instructor.max_daily_courses:
            return False
    
    # --- 3. Check Max Morning/Afternoon Courses ---
    
    # Get the schedule for this course's year and day
    day_schedule = year_schedule.get(slot_day, {}) # e.g., {"08:30-09:30": "ENE100", ...}
    
    m_courses = set()
    a_courses = set()

    # Find all slot objects for this day
    slots_for_day = [s for s in time_slots_map.values() if s.day == slot_day]
    
    # Count existing courses in morning/afternoon
    for s in slots_for_day:
        if s.time in day_schedule and day_schedule[s.time] is not None:
            # Get course code, remove instructor name if present
            course_code = day_schedule[s.time].split(" (")[0]
            if s.period == "morning":
                m_courses.add(course_code)
            elif s.period == "afternoon":
                a_courses.add(course_code)

    # Add the new course to the count
    new_period = time_slots_map[slot_ids[0]].period
    if new_period == "morning":
        m_courses.add(course.course_code)
    elif new_period == "afternoon":
        a_courses.add(course.course_code)
        
    # Check against config (assuming config is an object)
    if len(m_courses) > config.max_morning_courses:
        return False
    if len(a_courses) > config.max_afternoon_courses:
        return False
    
    # All checks passed
    return True