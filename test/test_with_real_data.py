# src/test_with_real_data.py
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from input_handler import load_data
from output_formatter import OutputFormatter

def test_with_real_data():
    """ทดสอบ Output Formatter ด้วยข้อมูลจริงจาก JSON"""
    print("🧪 ทดสอบ Output Formatter ด้วยข้อมูลจริง")
    print("=" * 50)
    
    try:
        # ใช้ข้อมูลจริงจาก JSON (ที่คนที่ 2 สร้าง)
        schedule = load_data("./data/data.json")
        
        # ทดสอบ Output Formatter ของคุณ
        formatter = OutputFormatter(schedule)
        
        print("📊 ทดสอบ display_summary():")
        formatter.display_summary()
        
        print("\n🎓 ทดสอบ display_schedule_by_year(1):")
        formatter.display_schedule_by_year(1)
        
        # print("\n👨‍🏫 ทดสอบ display_instructor_schedule('INT01'):")
        # formatter.display_instructor_schedule("INT01")
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        print("📌 สาเหตุอาจมาจาก:")
        print("   - ไฟล์ data.json ไม่存在")
        print("   - Data Structure ของคนที่ 1 ไม่ครบถ้วน")
        print("   - Input Handler ของคนที่ 2 มีปัญหา")

if __name__ == "__main__":
    test_with_real_data()