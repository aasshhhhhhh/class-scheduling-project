# src/test_data_structures.py
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from data_structures import Schedule
from input_handler import load_data  # ใช้ input handler ของคนที่ 2

def test_data_structure_with_real_data():
    """ทดสอบ Data Structure ด้วยข้อมูลจริงจาก JSON"""
    print("🧪 ทดสอบ Data Structure ของคนที่ 1 ด้วยข้อมูลจริง")
    print("=" * 60)
    
    try:
        # 1. โหลดข้อมูลจริงจาก JSON
        print("📥 กำลังโหลดข้อมูลจาก data.json...")
        schedule = load_data("./data/data.json")
        print(f"   ✅ โหลดข้อมูลสำเร็จ: {len(schedule.courses)} วิชา, {len(schedule.instructors)} อาจารย์")
        
        # 2. ตรวจสอบ method พื้นฐาน
        print("\n📋 1. ตรวจสอบ Method พื้นฐาน:")
        basic_methods = ['add_course', 'add_instructor', 'add_time_slot']
        missing_basic = []
        
        for method in basic_methods:
            if hasattr(schedule, method):
                print(f"   ✅ {method} : พบ")
            else:
                print(f"   ❌ {method} : ไม่พบ")
                missing_basic.append(method)
        
        # 3. ตรวจสอบ method สำหรับการจัดตาราง
        print("\n📋 2. ตรวจสอบ Method สำหรับการจัดตาราง:")
        scheduling_methods = ['assign_course_to_slot', 'get_course_at_timeslot']
        missing_scheduling = []
        
        for method in scheduling_methods:
            if hasattr(schedule, method):
                print(f"   ✅ {method} : พบ")
            else:
                print(f"   ❌ {method} : ไม่พบ")
                missing_scheduling.append(method)
        
        # 4. ตรวจสอบข้อมูลที่โหลดมา
        print("\n📋 3. ตรวจสอบข้อมูลที่โหลดมา:")
        
        # ตรวจสอบ courses
        if schedule.courses:
            sample_course = list(schedule.courses.values())[0]
            print(f"   ✅ มีข้อมูลวิชา: {len(schedule.courses)} วิชา")
            print(f"      ตัวอย่าง: {getattr(sample_course, 'course_code', 'N/A')} - {getattr(sample_course, 'course_name', 'N/A')}")
        else:
            print("   ❌ ไม่มีข้อมูลวิชา")
        
        # ตรวจสอบ instructors
        if schedule.instructors:
            sample_instructor = list(schedule.instructors.values())[0]
            print(f"   ✅ มีข้อมูลอาจารย์: {len(schedule.instructors)} คน")
            print(f"      ตัวอย่าง: {getattr(sample_instructor, 'instructorId', 'N/A')} - {getattr(sample_instructor, 'instructorName', 'N/A')}")
        else:
            print("   ❌ ไม่มีข้อมูลอาจารย์")
        
        # ตรวจสอบ time_slots
        if hasattr(schedule, 'time_slots') and schedule.time_slots:
            print(f"   ✅ มีข้อมูลช่วงเวลา: {len(schedule.time_slots)} ช่วง")
        else:
            print("   ❌ ไม่มีข้อมูลช่วงเวลา")
        
        # 5. ทดสอบการจัดตารางด้วยข้อมูลจริง
        print("\n📋 4. ทดสอบการจัดตารางด้วยข้อมูลจริง:")
        
        if schedule.courses and schedule.instructors and hasattr(schedule, 'time_slots') and schedule.time_slots:
            # เลือกวิชาและอาจารย์ตัวอย่างจากข้อมูลจริง
            sample_course_code = list(schedule.courses.keys())[0]
            sample_course = schedule.courses[sample_course_code]
            sample_instructor_id = sample_course.instructorId
            
            print(f"   วิชาตัวอย่าง: {sample_course_code}")
            print(f"   อาจารย์ตัวอย่าง: {sample_instructor_id}")
            
            # พยายามจัดตาราง
            if hasattr(schedule, 'assign_course_to_slot'):
                # หา slot ที่ว่างและอาจารย์ว่าง
                available_slots = []
                if sample_instructor_id in schedule.instructors:
                    instructor = schedule.instructors[sample_instructor_id]
                    for slot_id in instructor.available_slots:
                        if slot_id in schedule.time_slots and not schedule.time_slots[slot_id].is_occupied:
                            available_slots.append(slot_id)
                
                if available_slots:
                    test_slot = available_slots[0]
                    success = schedule.assign_course_to_slot(sample_course_code, test_slot)
                    print(f"   ✅ assign_course_to_slot: {success} (slot {test_slot})")
                else:
                    print("   ⚠️  ไม่มี slot ที่ว่างสำหรับทดสอบ")
            else:
                print("   ❌ assign_course_to_slot: ไม่มี method นี้")
                
            # ทดสอบการค้นหาวิชา
            if hasattr(schedule, 'get_course_at_timeslot'):
                sample_slot = list(schedule.time_slots.values())[0]
                course_info = schedule.get_course_at_timeslot(sample_slot.day, sample_slot.time)
                print(f"   ✅ get_course_at_timeslot: {course_info}")
            else:
                print("   ❌ get_course_at_timeslot: ไม่มี method นี้")
                
        else:
            print("   ⚠️  ไม่สามารถทดสอบได้เนื่องจากข้อมูลไม่ครบ")
        
        # 6. สรุปผล
        print("\n📊 สรุปผลการทดสอบ:")
        print("-" * 40)
        
        if not missing_basic and not missing_scheduling:
            print("   ✅ Data Structure ครบถ้วนสมบูรณ์")
            print("   ✅ พร้อมสำหรับการจัดตาราง")
            return True
        else:
            print("   ❌ Data Structure ไม่สมบูรณ์")
            if missing_basic:
                print(f"      - ขาด Method พื้นฐาน: {missing_basic}")
            if missing_scheduling:
                print(f"      - ขาด Method สำหรับจัดตาราง: {missing_scheduling}")
                print("      🚨 นี่คือปัญหาหลักที่ทำให้ระบบจัดตารางไม่ทำงาน!")
            return False
            
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการทดสอบ: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_specific_issues():
    """ทดสอบปัญหาจำเพาะ"""
    print("\n🔍 ทดสอบปัญหาจำเพาะ:")
    print("-" * 40)
    
    try:
        schedule = load_data("./data/data.json")
        
        # ทดสอบว่า courses เป็น dict หรือ list
        print(f"   ประเภทของ courses: {type(schedule.courses)}")
        if isinstance(schedule.courses, dict):
            print(f"   จำนวน courses: {len(schedule.courses)}")
        else:
            print(f"   จำนวน courses: {len(schedule.courses)} (เป็น list)")
        
        # ทดสอบ structure ของ course object
        if schedule.courses:
            first_course = list(schedule.courses.values())[0] if isinstance(schedule.courses, dict) else schedule.courses[0]
            print(f"   โครงสร้าง course object: {[attr for attr in dir(first_course) if not attr.startswith('_')]}")
        
    except Exception as e:
        print(f"   ❌ การทดสอบมีปัญหา: {e}")

if __name__ == "__main__":
    print("🔍 การทดสอบนี้ใช้ข้อมูลจริงจาก data.json เพื่อพิสูจน์ปัญหาของคนที่ 1\n")
    
    # รันการทดสอบหลัก
    success = test_data_structure_with_real_data()
    
    # รันการทดสอบปัญหาจำเพาะ
    test_specific_issues()
    
    print("\n" + "="*60)
    if success:
        print("🎉 ข้อสรุป: Data Structure ครบถ้วน - ปัญหาอยู่ที่ส่วนอื่น")
    else:
        print("🚨 ข้อสรุป: ยืนยันแล้ว! คนที่ 1 ทำ Data Structure ไม่ครบถ้วน")
        print("   ต้องการ method สำหรับการจัดตารางเพิ่มเติม")