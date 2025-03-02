"""Python file to generate schedule based on the availability of the employee"""

import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict


class Employee:
    """Class to store information related to employee and their shift preferences"""

    def __init__(self, name, preferences):
        self.name = name
        self.preferences = preferences  # {day: (priority1, priority2)}
        self.assigned_days = 0  # Track number of days assigned
        self.assigned_shifts = {}  # Track assigned shifts per day

    def reset_assigned_days(self):
        """Reset assigned shifts to generate a new schedule."""
        self.assigned_days = 0
        self.assigned_shifts = {}


class EmployeeScheduler:
    """Scheduler to assign shifts based on input."""

    def __init__(self, gui):
        """Initialize the scheduler and setup UI components."""
        self.root = gui
        self.root.title("Employee Shift Scheduler")
        self.root.geometry("425x850")

        self.employees = []  # Store lists of employees
        # {day: {shift: [employees]}}
        self.schedule = defaultdict(lambda: defaultdict(list))
        self.max_shifts_per_week = 5
        self.days = ["Monday", "Tuesday", "Wednesday",
                     "Thursday", "Friday", "Saturday", "Sunday"]
        self.shifts = ["None", "Morning", "Afternoon", "Evening"]

        self.setup_ui()

    def setup_ui(self):
        """Setup the UI for entering employee information."""
        style = ttk.Style()
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Employee Name:").grid(
            row=0, column=0, pady=5, sticky=tk.W)
        self.name_entry = tk.Entry(frame, bd=2, width=38)
        self.name_entry.grid(row=0, column=1, columnspan=2, pady=5)

        self.shift_dict = {}
        for row, day in enumerate(self.days, start=1):
            ttk.Label(frame, text=f"{day}:").grid(
                row=row, column=0, pady=5, sticky=tk.W)

            priority1_var = tk.StringVar(value="None")
            priority2_var = tk.StringVar(value="None")

            ttk.Combobox(frame, state='readonly', textvariable=priority1_var,
                         values=self.shifts, width=12).grid(row=row, column=1, pady=2)
            ttk.Combobox(frame, state='readonly', textvariable=priority2_var,
                         values=self.shifts, width=12).grid(row=row, column=2, pady=2)

            self.shift_dict[day] = (priority1_var, priority2_var)

        style.configure('TButton', font=('Garamond', 13, 'bold'),
                        foreground='blue', background='green')
        ttk.Button(frame, text="Add Employee", style='TButton', width=20,
                   command=self.add_employee).grid(row=row+1, column=0, columnspan=3, pady=5)
        ttk.Button(frame, text="Generate Schedule", style='TButton', width=20,
                   command=self.generate_schedule).grid(row=row+2, column=0, columnspan=3, pady=2)
        ttk.Button(frame, text="Reset Employees", style='TButton', width=20,
                   command=self.reset_employees).grid(row=row+3, column=0, columnspan=3, pady=2)

        self.output_schedule = tk.Text(
            frame, height=30, width=50, relief='solid', wrap=tk.WORD, state=tk.DISABLED)
        self.output_schedule.grid(row=row+4, column=0, columnspan=3, pady=10)

    def add_employee(self):
        """Add employee along with their shift preferences."""
        name = self.name_entry.get()
        preferences = {day: (self.shift_dict[day][0].get(
        ), self.shift_dict[day][1].get()) for day in self.days}

        if name.strip():
            self.employees.append(Employee(name, preferences))
            messagebox.showinfo(
                "Success", f"Employee {name} added successfully!")
        else:
            messagebox.showerror(
                "Error", "Please enter a valid name and select shift preferences for each day.")

    def reset_employees(self):
        """Remove all employees and reset the schedule."""
        self.employees.clear()
        messagebox.showinfo("Reset", "All employees have been removed.")
        self.output_schedule.config(state=tk.NORMAL)
        self.output_schedule.delete('1.0', tk.END)
        self.output_schedule.config(state=tk.DISABLED)

    def generate_schedule(self):
        """Generate a shift schedule based on employee preferences."""
        self.schedule.clear()
        for emp in self.employees:
            emp.reset_assigned_days()   # Reset all assigned shift days for new schedule

        for emp in self.employees:
            # Check if the employee have max shift already allocated
            # If yes, then continue to next employee
            if emp.assigned_days >= self.max_shifts_per_week:
                continue

            for day, (priority1, priority2) in emp.preferences.items():
                if emp.assigned_days >= self.max_shifts_per_week:
                    break

                if priority1 == "None" and priority2 == "None":
                    continue

                # Check if the employee has already been assigned a shift for this day
                # Assign the shift if there is no assigned shift for this day.
                if day not in emp.assigned_shifts:
                    available_shifts = [s for s in [
                        priority1, priority2] if s != "None"]
                    assigned = False

                    # Assign the shift to the employee if there is space available in their preferred shift
                    for shift in available_shifts:
                        if len(self.schedule[day][shift]) < 2:
                            self.schedule[day][shift].append(emp.name)
                            emp.assigned_shifts[day] = shift
                            emp.assigned_days += 1
                            assigned = True
                            break

                    # IF THERE ARE NO PREFERRED SHIFT FOR THAT DAY
                    # Assign the next available shift on that day to the employee
                    if not assigned:
                        for shift in self.shifts:
                            if shift != "None" and shift not in available_shifts and len(self.schedule[day][shift]) < 2:
                                self.schedule[day][shift].append(emp.name)
                                emp.assigned_shifts[day] = shift
                                emp.assigned_days += 1
                                assigned = True
                                break

                    # If there is no space available on any shift that day,
                    # assign the preferred shift on next available day
                    if not assigned:
                        for next_day in self.days[self.days.index(day) + 1:]:
                            emp.assigned_shifts[next_day] = "None"
                            if emp.assigned_days >= self.max_shifts_per_week:
                                break

                            for shift in available_shifts:
                                if len(self.schedule[next_day][shift]) < 2:
                                    self.schedule[next_day][shift].append(
                                        emp.name)
                                    emp.assigned_shifts[next_day] = shift
                                    emp.assigned_days += 1
                                    assigned = True
                                    break
                            if assigned:
                                break

        self.display_schedule()

    def display_schedule(self):
        """Display the generated schedule."""
        self.output_schedule.config(state=tk.NORMAL)
        self.output_schedule.delete("1.0", tk.END)
        for day, shifts in self.schedule.items():
            self.output_schedule.insert(tk.END, f"{day}\n")
            for shift, employees in shifts.items():
                self.output_schedule.insert(
                    tk.END, f"  {shift}: {', '.join(employees)}\n")
            self.output_schedule.insert(tk.END, "\n")
        self.output_schedule.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeScheduler(root)
    root.mainloop()
