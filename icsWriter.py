class ICSWriter:
    def __init__(self, save_path):
        self.save_path = save_path
        self.ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Custom Python Script//EN\n"

    def add_event(self, title, days, start_time, end_time, semester_start, semester_end, location="Carleton University", description=None):
        from datetime import datetime, timedelta

        # Helper to calculate the first date of an event
        def get_first_date(weekday_name, start_date):
            weekday_map = {
                "Sunday": 6, "Monday": 0, "Tuesday": 1, "Wednesday": 2, 
                "Thursday": 3, "Friday": 4, "Saturday": 5
            }
            start_day = start_date.weekday()
            target_day = weekday_map[weekday_name]
            delta_days = (target_day - start_day) % 7
            return start_date + timedelta(days=delta_days)

        # Calculate event details
        first_date = get_first_date(days[0], semester_start)
        start_datetime = datetime.combine(first_date, datetime.strptime(start_time, "%H:%M").time())
        end_datetime = datetime.combine(first_date, datetime.strptime(end_time, "%H:%M").time())
        
        dtstart = start_datetime.strftime("%Y%m%dT%H%M%S")
        dtend = end_datetime.strftime("%Y%m%dT%H%M%S")
        until = semester_end.strftime("%Y%m%dT%H%M%S")
        byday = ",".join(day[:2].upper() for day in days)

        # Write event with recurrence rule
        self.ics_content += (
            "BEGIN:VEVENT\n"
            f"SUMMARY:{title}\n"
            f"DTSTART:{dtstart}\n"
            f"DTEND:{dtend}\n"
            f"LOCATION:{location}\n"
            f"DESCRIPTION:{description or ''}\n"
            f"RRULE:FREQ=WEEKLY;BYDAY={byday};UNTIL={until}\n"
            "END:VEVENT\n"
        )

    def save(self):
        self.ics_content += "END:VCALENDAR\n"
        with open(self.save_path, "w") as file:
            file.write(self.ics_content)
