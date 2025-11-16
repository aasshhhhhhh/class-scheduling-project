# \test\test-scheduler.py

import os
import sys

sys.path.append(os.path.dirname(__file__))

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))

if src_path not in sys.path:
    sys.path.append(src_path)

try:
    from scheduler import Scheduler
except ImportError:
    print(f"❌ Can not import 'scheduler' from: {src_path}")
    sys.exit(1)

my_scheduler = Scheduler()
slot_ids = my_scheduler.find_continuous_slots(instructor_id="INT01", study_hours=3)
print(slot_ids)
