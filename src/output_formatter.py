class OutputFormatter:
    def __init__(self, schedule):
        self.schedule = schedule
        # กำหนดวันและช่วงเวลามาตรฐานสำหรับแสดงผล
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.time_slots = [
            '08:30-09:30', '09:30-10:30', '10:30-11:30', '11:30-12:30',
            '13:30-14:30', '14:30-15:30', '15:30-16:30', '16:30-17:30'
        ]


    def display_schedule_by_year(self, year):
        """แสดงตารางเรียนสำหรับปีที่กำหนด"""
        print(f"\n🎓 Year {year}")
        print("=" * 60)

        for day in self.days:
            print(f"\n📅 {day}:")
            print("-" * 40)

            for time_slot in self.time_slots: # ตรวจว่า เวลานี้ วันนี้ มีเรียนไหม?
                schedule_info = self._get_course_info(year, day, time_slot)
                
                # กำหนดพักเที่ยง
                if time_slot == '11:30-12:30':
                    print(f"  🕛 {time_slot} : 🍽️  Lunch break")
                
                # กรณีมีเรียน: แสดงชื่อวิชาและอาจารย์
                elif schedule_info:
                    instructor = self.schedule.instructors[schedule_info['instructor']]
                    print(f"  🕐 {time_slot} : 📚 {schedule_info['course']} - {instructor.instructorName}")
                else:
                    print(f"  🕐 {time_slot} : 🆓 Free") # กรณีไม่มีเรียน


    def _get_course_info(self, year, day, time):
        """ค้นหาว่าวัน เวลา ปีนี้มีวิชาอะไรบ้าง (ใช้ method หลักก่อน ถ้าไม่มีใช้วิธีสำรอง)"""

        # วิธีที่ 1: ถ้าใน Schedule มีฟังก์ชันค้นหาเร็วๆ ให้ใช้ก่อน (Best Practice)
        if hasattr(self.schedule, 'get_course_at_timeslot'):
            result = self.schedule.get_course_at_timeslot(year, day, time)
            if result:
                return result
    
        # ถ้าไม่มีฟังก์ชันค้นหา ไล่ดูวิชาทั้งหมดในระบบ (Manual Search)
        for course in self.schedule.courses.values():
                if course.year != year: # ข้ามถ้าไม่ใช่วิชาของปีที่ต้องการหา
                    continue
                
                # เช็กสล็อตเวลาของวิชานั้นๆ ว่าตรงกับวัน/เวลาที่ต้องการไหม
                for slot_id in course.scheduled_slots:
                    if slot_id in self.schedule.time_slots:
                        slot = self.schedule.time_slots[slot_id]
                        if slot.day == day and slot.time == time:
                            return {
                                'course': course.course_code,
                                'instructor': course.instructorId
                            }
        return None 