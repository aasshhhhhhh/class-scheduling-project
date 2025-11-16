# src/check_original.py
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# นำเข้าโค้ดเดิมของคนที่ 1 (ไม่ต้องแก้ไขอะไร)
from data_structures import Schedule

def test_original_data_structure():
    """ทดสอบว่า Data Structure เดิมของคนที่ 1 ครบถ้วนไหม"""
    print("🧪 ทดสอบ Data Structure เดิมของคนที่ 1")
    print("=" * 50)
    
    schedule = Schedule()
    
    # ตรวจสอบว่ามี method จำเป็นเหล่านี้ไหม
    required_methods = [
        'add_course',
        'add_instructor', 
        'add_time_slot',
        'assign_course_to_slot',
        'get_course_at_timeslot'  # ← นี้คือตัวปัญหา!
    ]
    
    print("📋 ตรวจสอบ method ที่จำเป็น:")
    missing_methods = []
    
    for method in required_methods:
        if hasattr(schedule, method):
            print(f"   ✅ {method} : พบ")
        else:
            print(f"   ❌ {method} : ไม่พบ")
            missing_methods.append(method)
    
    if missing_methods:
        print(f"\n🚨 พบ method ที่ขาดหาย: {missing_methods}")
        print("   นี่คือปัญหาของคนที่ 1 (Data Structure Designer)")
    else:
        print(f"\n✅ Data Structure ของคนที่ 1 ครบถ้วน")
        print("   ปัญหาอาจอยู่ที่ส่วนอื่น")

if __name__ == "__main__":
    test_original_data_structure()