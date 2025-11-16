
# src/output_formatter.py
from data_structures import Schedule

class OutputFormatter:
    def __init__(self, schedule):
        self.schedule = schedule
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.time_slots = [
            '08:30-09:30', '09:30-10:30', '10:30-11:30', '11:30-12:30',
            '13:30-14:30', '14:30-15:30', '15:30-16:30', '16:30-17:30'
        ]

    def display_schedule_by_year(self, year):
        """แสดงตารางเรียนสำหรับปีที่กำหนด"""
        print(f"\n🎓 ตารางเรียนปี {year}")
        print("=" * 60)

        for day in self.days:
            print(f"\n📅 {day}:")
            print("-" * 40)

            has_class = False
            for time_slot in self.time_slots:
                # ใช้ฟังก์ชันสำรองถ้า get_course_at_timeslot ไม่มี
                schedule_info = self._get_course_info(year, day, time_slot)
                
                if time_slot == '11:30-12:30':
                    print(f"  🕛 {time_slot} : 🍽️ พักเที่ยง")
                elif schedule_info:
                    course = self.schedule.courses[schedule_info['course']]
                    instructor = self.schedule.instructors[schedule_info['instructor']]
                    print(f"  🕐 {time_slot} : 📚 {schedule_info['course']} - {instructor.instructorName}")
                    has_class = True
                else:
                    print(f"  🕐 {time_slot} : 🆓 ว่าง")

            if not has_class:
                print("  🆓 ไม่มีเรียนทั้งวัน")

    def _get_course_info(self, year, day, time):
        """หาข้อมูลวิชาในวันและเวลาที่กำหนด (สำรอง)"""
    # ลองใช้ฟังก์ชันหลักก่อน
        if hasattr(self.schedule, 'get_course_at_timeslot'):
            result = self.schedule.get_course_at_timeslot(year, day, time)
            if result:
                return result
    
    # ถ้าไม่มี ให้ใช้วิธีค้นหาทั้งหมด
        for course in self.schedule.courses.values():
            if course.year != year:
                continue
            
        for slot_id in course.scheduled_slots:
            if slot_id in self.schedule.time_slots:
                slot = self.schedule.time_slots[slot_id]
                if slot.day == day and slot.time == time:
                    return {
                        'course': course.course_code,
                        'instructor': course.instructorId
                    }
        return None

    def display_instructor_schedule(self, instructor_id):
        """แสดงตารางสอนของอาจารย์"""
        instructor = self.schedule.instructors.get(instructor_id)
        if not instructor:
            print(f"❌ ไม่พบอาจารย์ ID: {instructor_id}")
            return

        print(f"\n👨‍🏫 ตารางสอนอาจารย์: {instructor.instructorName} ({instructor.department})")
        print(f"📊 สอนแล้ว: {instructor.assigned_hours} ชั่วโมง/สัปดาห์")
        print("=" * 50)

        for day in self.days:
            print(f"\n📅 {day}:")
            print("-" * 30)

            has_teaching = False
            for time_slot in self.time_slots:
                # ข้ามเวลาพักเที่ยง
                if time_slot == '11:30-12:30':
                    continue

                # หาวิชาที่อาจารย์สอนในเวลานี้
                for course_code in instructor.assigned_courses:
                    course = self.schedule.courses[course_code]
                    for slot_id in course.scheduled_slots:
                        slot = self.schedule.time_slots[slot_id]
                        if slot.day == day and slot.time == time_slot:
                            print(f"  {time_slot} : {course_code} ({course.course_name})")
                            has_teaching = True
                            break

            if not has_teaching:
                print("  🆓 ไม่มีสอน")

    def display_summary(self):
        """แสดงสรุปข้อมูล"""
        print("\n📊 สรุปตารางเรียน")
        print("=" * 50)

        total_courses = len(self.schedule.courses)
        assigned_courses = sum(1 for course in self.schedule.courses.values() if course.scheduled_slots)
        total_assigned_hours = sum(len(course.scheduled_slots) for course in self.schedule.courses.values())

        print(f"📚 จำนวนวิชาทั้งหมด: {total_courses} วิชา")
        print(f"✅ วิชาที่จัดตารางแล้ว: {assigned_courses} วิชา")
        print(f"❌ วิชาที่ยังไม่ได้จัด: {total_courses - assigned_courses} วิชา")
        print(f"⏰ ชั่วโมงเรียนที่จัดแล้ว: {total_assigned_hours} ชั่วโมง")
        print(f"👨‍🏫 จำนวนอาจารย์: {len(self.schedule.instructors)} คน")

        # สรุปตามปี
        print("\n🎓 สรุปตามปีการศึกษา:")
        for year in range(1, 5):
            year_courses = [c for c in self.schedule.courses.values() if c.year == year and c.scheduled_slots]
            year_hours = sum(len(c.scheduled_slots) for c in year_courses)
            print(f"  ปี {year}: {len(year_courses)} วิชา, {year_hours} ชั่วโมง")

        # สรุปตามอาจารย์
        print("\n👨‍🏫 สรุปตามอาจารย์:")
        for instructor in self.schedule.instructors.values():
            status = "✅ พร้อมสอน" if instructor.assigned_hours > 0 else "⏳ รอการจัด"
            print(f"  {instructor.instructorName}: {instructor.assigned_hours}/{instructor.max_weekly_hours} ชั่วโมง {status}")