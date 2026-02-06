from datetime import datetime, timedelta

class InputTimeTracker:
    def __init__(self):
        self.last_input_time = None

    def check_time_gap(self):
        now = datetime.utcnow()

        if self.last_input_time is None:
            self.last_input_time = now
            print("[DEBUG][TIME] First input detected")
            return "first_input"

        time_diff = now - self.last_input_time
        self.last_input_time = now

        print(f"[DEBUG][TIME] Time gap → {time_diff}")

        if time_diff <= timedelta(minutes=30):
            print("[DEBUG][TIME] Gap ≤ 30 minutes → SAME EPISODE")
            return "less_than_30_minutes"
        else:
            print("[DEBUG][TIME] Gap > 30 minutes → NEW EPISODE")
            return "greater_than_30_minutes"
