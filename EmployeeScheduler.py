"""Python file to generate schedule based on the availability of the employee"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import defaultdict


class Employee:
    """Class to store information related to employee and their shift preferences"""

    def __init__(self, name, preferences):
        self.name = name
        # Store shift priority preference as dict {day: (priority1, priority2)}
        self.preferences = preferences
        self.assigned_days = 0              # Track number of days assigned
        self.assigned_shifts = {}           # Track assigned shifts per day

    def reset_assigned_days(self):
        """Reset assigned shifts to generate new schdeule based on more information"""
        self.assigned_days = 0
        self.assigned_shifts = {}


class EmployeeScheduler:
    """Scheduler to shifts based on the input"""

    def __init__(self, gui):
        self.root = gui
        self.root.title("Employee Shift Scheduler")
        self.root.geometry("425x850")

        self.employees = []  # Stores list of Employee objects
        # {day: {shift: [employees]}}
        self.schedule = defaultdict(lambda: defaultdict(list))
        self.max_shifts_per_week = 5
        self.days = ["Monday", "Tuesday", "Wednesday",
                     "Thursday", "Friday", "Saturday", "Sunday"]

        self.setup_ui()

    def setup_ui(self):
        """Setup a UI for user to enter employee information"""
        # Create style Object
        style = ttk.Style()
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create a label and entry for user to enter employee name
        ttk.Label(frame, text="Employee Name:").grid(
            row=0, column=0, pady=5, sticky=tk.W)
        self.name_entry = tk.Entry(frame, bd=2, width=38)
        self.name_entry.grid(row=0, column=1, columnspan=2, pady=5)

        self.shift_dict = {}
        row = 1
        for day in self.days:
            ttk.Label(frame, text=f"{day}:").grid(
                row=row, column=0, pady=5, sticky=tk.W)

            priority1_var = tk.StringVar(value="Morning")
            priority2_var = tk.StringVar(value="Afternoon")

            available_shift = ["Morning", "Afternoon", "Evening"]
            ttk.Combobox(frame, state='readonly', textvariable=priority1_var, values=available_shift, width=12).grid(
                row=row, column=1, pady=2)
            ttk.Combobox(frame, state='readonly', textvariable=priority2_var, values=available_shift, width=12).grid(
                row=row, column=2, pady=2)

            self.shift_dict[day] = (priority1_var, priority2_var)
            row += 1

        # Adding style to Pushbutton to highlight it.
        style.configure('TButton', font=('Garamond', 13, 'bold'),
                        foreground='blue', background='green')
        ttk.Button(frame, text="Add Employee", style='TButton', width=20,
                   command=self.add_employee).grid(row=row, column=0, columnspan=3, pady=5)
        ttk.Button(frame, text="Generate Schedule", style='TButton', width=20,
                   command=self.generate_schedule).grid(row=row+1, column=0, columnspan=3, pady=2)
        ttk.Button(frame, text="Reset Employees", style='TButton', width=20,
                   command=self.reset_employees).grid(row=row+2, column=0, columnspan=3, pady=2)

        self.output_schedule = tk.Text(
            frame, height=30, width=50, relief='solid', wrap=tk.WORD, state=tk.DISABLED)
        self.output_schedule.grid(row=row+3, column=0, columnspan=3, pady=10)

    def add_employee(self):
        """Add employee along with their preferences on the list"""
        name = self.name_entry.get()
        preferences = {day: (self.shift_dict[day][0].get(
        ), self.shift_dict[day][1].get()) for day in self.days}

        if name and preferences:
            self.employees.append(Employee(name, preferences))
            messagebox.showinfo(
                "Success", f"Employee {name} is added successfully to the list!")
        else:
            messagebox.showerror(
                "Error", "Please enter a valid name and select shift preferences for each day.")

    def reset_employees(self):
        """Remove all the employees from the list"""
        self.employees.clear()
        messagebox.showinfo("Reset", "All employees have been removed.")

    def generate_schedule(self):
        """Generate appropriate schedule for all available employees"""
        self.schedule.clear()
        for employee in self.employees:
            employee.reset_assigned_days()

        for day in self.days:
            for shift in ["Morning", "Afternoon", "Evening"]:
                assigned_employees = []

                # Try to assign employees based on their priority
                for emp in self.employees:
                    if emp.assigned_days < self.max_shifts_per_week and shift in emp.preferences[day]:
                        if day not in emp.assigned_shifts:
                            emp.assigned_shifts[day] = shift
                            emp.assigned_days += 1
                            assigned_employees.append(emp.name)

                    if len(assigned_employees) >= 2:
                        break

                # If fewer than 2 employees, assign randomly from those with available slots
                if len(assigned_employees) < 2:
                    available_employees = [emp for emp in self.employees if emp.assigned_days <
                                           self.max_shifts_per_week and day not in emp.assigned_shifts]
                    random.shuffle(available_employees)
                    for emp in available_employees:
                        emp.assigned_shifts[day] = shift
                        emp.assigned_days += 1
                        assigned_employees.append(emp.name)
                        if len(assigned_employees) >= 2:
                            break

                self.schedule[day][shift] = assigned_employees

        self.display_schedule()

    def display_schedule(self):
        """Display generated schedule"""
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
