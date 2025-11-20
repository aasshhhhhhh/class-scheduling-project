import os
import sys

sys.path.append(os.path.dirname(__file__))

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))

if src_path not in sys.path:
    sys.path.append(src_path)

try:
    from input_handler import load_data
except ImportError:
    print(f"❌ Can not import 'scheduler' from: {src_path}")
    sys.exit(1)

# Testing
if __name__ == "__main__":
    # ใช้ path จำลอง หรือปรับเป็น path ที่ถูกต้อง
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "data.json")

    try:
        my_schedule = load_data(data_path)
        
        print(f"Loaded {len(my_schedule.courses)} courses")

        year_counts = {}
        total_hours = {}

        for course in my_schedule.courses.values():
            y = course.year
            if y in year_counts:
                year_counts[y] += 1
            else:
                year_counts[y] = 1

            h = course.study_hours
            if y in total_hours:
                total_hours[y] += h
            else:
                total_hours[y] = h

        print("\n--- Courses per Year and Total Study Hours per Year ---")
        for year in sorted(year_counts.keys()):
            count = year_counts[year]   
            hours = total_hours[year]   
            
            print(f"  - Year {year}: {count} courses, Total {hours} hours")

        print(f"Loaded {len(my_schedule.time_slots)} slots")
        print(f"Loaded {len(my_schedule.instructors)} instructors")

        print("\n--- Configuration ---")
        # Loop through all attributes in the Config object automatically
        for key, value in vars(my_schedule.config).items():
            print(f"Config {key}: {value}")
        
    except Exception as e:
        print(f"\nAn error occurred during loading or validation: {e}")