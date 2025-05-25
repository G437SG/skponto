from datetime import datetime, timedelta

class Timesheet:
    def __init__(self, user_id):
        self.user_id = user_id
        self.entries = []

    def clock_in(self):
        entry = {
            'clock_in_time': datetime.now(),
            'clock_out_time': None,
            'hours_worked': 0
        }
        self.entries.append(entry)

    def clock_out(self):
        if not self.entries or self.entries[-1]['clock_out_time'] is not None:
            raise Exception("User must clock in before clocking out.")
        
        self.entries[-1]['clock_out_time'] = datetime.now()
        self.entries[-1]['hours_worked'] = self.calculate_hours(self.entries[-1])

    def calculate_hours(self, entry):
        if entry['clock_out_time'] is None:
            return 0
        return (entry['clock_out_time'] - entry['clock_in_time']).total_seconds() / 3600

    def get_total_hours(self):
        total_hours = sum(entry['hours_worked'] for entry in self.entries)
        return total_hours

    def get_overtime_hours(self):
        total_hours = self.get_total_hours()
        if total_hours > 9:
            return total_hours - 9
        return 0

    def get_entries(self):
        return self.entries