import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime, timedelta
from icsWriter import ICSWriter

class ICSGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ICS Generator")

        # UI Variables
        self.title_var = tk.StringVar()
        self.start_time_var = tk.StringVar()
        self.end_time_var = tk.StringVar()
        self.color_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.day_vars = {day: tk.BooleanVar() for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
        self.classes = []  # Store all added classes

        # Build UI
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="Class Title:").grid(row=0, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.title_var).grid(row=0, column=1, sticky="ew")

        tk.Label(self.root, text="Days:").grid(row=1, column=0, sticky="w")
        for idx, (day, var) in enumerate(self.day_vars.items()):
            tk.Checkbutton(self.root, text=day, variable=var).grid(row=1, column=1+idx, sticky="w")

        tk.Label(self.root, text="Start Time (HH:MM):").grid(row=2, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.start_time_var).grid(row=2, column=1, sticky="ew")

        tk.Label(self.root, text="End Time (HH:MM):").grid(row=3, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.end_time_var).grid(row=3, column=1, sticky="ew")

        tk.Label(self.root, text="Color:").grid(row=4, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.color_var).grid(row=4, column=1, sticky="ew")

        tk.Label(self.root, text="Semester Start Date (YYYY-MM-DD):").grid(row=5, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.start_date_var).grid(row=5, column=1, sticky="ew")

        tk.Label(self.root, text="Semester End Date (YYYY-MM-DD):").grid(row=6, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.end_date_var).grid(row=6, column=1, sticky="ew")

        # Buttons
        tk.Button(self.root, text="Add Class", command=self.add_class).grid(row=7, column=0, pady=5)
        tk.Button(self.root, text="Generate .ics", command=self.generate_ics).grid(row=7, column=1, pady=5)

        self.root.grid_columnconfigure(1, weight=1)

    def add_class(self):
        try:
            # Collect inputs
            title = self.title_var.get()
            days = [day for day, var in self.day_vars.items() if var.get()]
            start_time = self.start_time_var.get()
            end_time = self.end_time_var.get()
            color = self.color_var.get()

            if not title or not days or not start_time or not end_time:
                messagebox.showerror("Error", "Please fill in all required fields.")
                return

            # Validate time format
            datetime.strptime(start_time, "%H:%M")
            datetime.strptime(end_time, "%H:%M")

            # Check for conflicts
            for existing_class in self.classes:
                for day in days:
                    if day in existing_class["days"] and self.check_time_conflict(start_time, end_time, existing_class["start_time"], existing_class["end_time"]):
                        messagebox.showerror("Conflict Detected", f"Conflict with class '{existing_class['title']}' on {day}.")
                        return

            # Add class to the list
            self.classes.append({
                "title": title,
                "days": days,
                "start_time": start_time,
                "end_time": end_time,
                "color": color,
            })
            messagebox.showinfo("Success", f"Class '{title}' added successfully!")

            # Reset fields
            self.title_var.set("")
            for var in self.day_vars.values():
                var.set(False)
            self.start_time_var.set("")
            self.end_time_var.set("")
            self.color_var.set("")

        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Use HH:MM.")

    def generate_ics(self):
        try:
            # Ensure start and end dates are provided
            semester_start = datetime.strptime(self.start_date_var.get(), "%Y-%m-%d")
            semester_end = datetime.strptime(self.end_date_var.get(), "%Y-%m-%d")

            if not self.classes:
                messagebox.showerror("Error", "No classes added. Please add classes before generating.")
                return

            # Get file save location
            save_path = filedialog.asksaveasfilename(defaultextension=".ics", filetypes=[("iCalendar files", "*.ics")])
            if not save_path:
                return

            # Generate ICS file
            writer = ICSWriter(save_path)
            for class_info in self.classes:
                writer.add_event(
                    class_info["title"],
                    class_info["days"],
                    class_info["start_time"],
                    class_info["end_time"],
                    semester_start,
                    semester_end,
                    description=f"Category: {class_info['color']}",
                )
            writer.save()

            messagebox.showinfo("Success", f".ics file saved at {save_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    @staticmethod
    def check_time_conflict(start1, end1, start2, end2):
        start1 = datetime.strptime(start1, "%H:%M")
        end1 = datetime.strptime(end1, "%H:%M")
        start2 = datetime.strptime(start2, "%H:%M")
        end2 = datetime.strptime(end2, "%H:%M")
        return max(start1, start2) < min(end1, end2)
