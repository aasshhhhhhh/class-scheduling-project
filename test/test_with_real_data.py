import os
import sys

# --- 1. แก้ไข Path ---
# ได้ .../Project_Root/test
current_dir = os.path.dirname(os.path.abspath(__file__))
# ได้ .../Project_Root
project_root = os.path.dirname(current_dir) 

# สร้าง Path ไปยัง src
src_path = os.path.join(project_root, 'src')
# เพิ่ม .../Project_Root/src เข้าไปใน sys.path
sys.path.insert(0, src_path) 

# --- 2. แก้ไข Imports (ตอนนี้ Python จะหาเจอแล้ว) ---
try:
    from input_handler import load_data
    from output_formatter import OutputFormatter
except ModuleNotFoundError:
    print(f"❌ ยังหา Module ไม่เจอ, ตรวจสอบว่า 'src' path ถูกต้อง: {src_path}")
    sys.exit(1)


def test_with_real_data():
    """ทดสอบ Output Formatter ด้วยข้อมูลจริงจาก JSON"""
    print("🧪 ทดสอบ Output Formatter ด้วยข้อมูลจริง")
    print("=" * 50)
    
    try:
        # --- 3. แก้ไข Path ของ data.json ---
        # สร้าง Path แบบเต็มไปยัง data.json โดยอิงจาก Project Root
        data_path = os.path.join(project_root, "data", "data.json")
        
        print(f"Loading data from: {data_path}")
        schedule = load_data(data_path)
        
        formatter = OutputFormatter(schedule)
        
        print("📊 ทดสอบ display_summary():")
        formatter.display_summary()
        
        # print("\n🎓 ทดสอบ display_schedule_by_year(1):")
        # formatter.display_schedule_by_year(1)
        for year_to_display in range(1, 5): # วนลูป 1, 2, 3, 4
            formatter.display_schedule_by_year(year_to_display)
        
        # print("\n👨‍🏫 ทดสอบ display_instructor_schedule('INT01'):")
        # formatter.display_instructor_schedule("INT01")
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        print("📌 สาเหตุอาจมาจาก:")
        print(f"   - หาไฟล์ data.json ไม่เจอที่: {data_path}")
        print("   - Data Structure (src/data_structures.py) ไม่ครบถ้วน")
        print("   - Input Handler (src/input_handler.py) มีปัญหา")

if __name__ == "__main__":
    test_with_real_data()