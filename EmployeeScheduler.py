import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import defaultdict

class Employee:
    def __init__(self, name, preferences):
        self.name = name
        # Store shift priority preference as dict {day: (priority1, priority2)}
        self.preferences = preferences

class EmployeeScheduler:
    """Scheduler to schedule shifts based on the input"""
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Shift Scheduler")
        self.root.geometry("425x580")

        self.employees = []  # Stores list of Employee objects
        self.schedule = defaultdict(lambda: defaultdict(list))  # {day: {shift: [employees]}}
        self.max_shifts_per_week = 5
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        self.setup_ui()

    def setup_ui(self):
        """Setup a UI for user to enter employee information"""
        # Create style Object
        style = ttk.Style()
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Employee Name:").grid(row=0, column=0, pady=5, sticky=tk.W)
        self.name_entry = tk.Entry(frame, bd=2, width=38)
        self.name_entry.grid(row=0, column=1, columnspan=2, pady=5)

        self.shift_dict = {}
        row = 1
        for day in self.days:
            ttk.Label(frame, text=f"{day}:").grid(row=row, column=0, pady=5, sticky=tk.W)

            priority1_var = tk.StringVar(value="Morning")
            priority2_var = tk.StringVar(value="Afternoon")

            available_shift = ["Morning", "Afternoon", "Evening"]
            ttk.Combobox(frame, textvariable=priority1_var, values=available_shift, width=12).grid(row=row, column=1, pady=2)
            ttk.Combobox(frame, textvariable=priority2_var, values=available_shift, width=12).grid(row=row, column=2, pady=2)

            self.shift_dict[day] = (priority1_var, priority2_var)
            row += 1

        # Will add style to every available button
        # even though we are not passing style to every button widget.
        style.configure('TButton', font=('Garamond', 13, 'bold'))
        ttk.Button(frame, text="Add Employee", style='TButton', width=20, command=self.add_employee).grid(row=row, column=0, columnspan=3, pady=5)
        ttk.Button(frame, text="Generate Schedule", style='TButton', width=20, command=self.generate_schedule).grid(row=row+1, column=0, columnspan=3, pady=2)
        
        self.output_text = tk.Text(frame, height=15, width=50, wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.grid(row=row+2, column=0, columnspan=3, pady=10)
    
    def add_employee(self):
        name = self.name_entry.get()
        preferences = {day: (self.shift_dict[day][0].get(), self.shift_dict[day][1].get()) for day in self.days}
        
        if name and preferences:
            self.employees.append(Employee(name, preferences))
            messagebox.showinfo("Success", f"Employee {name} added successfully!")
        else:
            messagebox.showerror("Error", "Please enter a valid name and select shift preferences for each day.")
    
    def generate_schedule(self):
        employee_shifts = defaultdict(int)  # Track shifts assigned to employees
        self.schedule.clear()
        
        for day in self.days:
            for shift in ["Morning", "Afternoon", "Evening"]:
                available_employees = [emp for emp in self.employees if (shift in emp.preferences[day]) and employee_shifts[emp.name] < self.max_shifts_per_week]
                
                if len(available_employees) < 2:
                    additional_employees = [emp for emp in self.employees if employee_shifts[emp.name] < self.max_shifts_per_week and emp not in available_employees]
                    random.shuffle(additional_employees)
                    available_employees.extend(additional_employees[:(2 - len(available_employees))])
                
                for emp in available_employees[:3]:  # Assign up to 3 employees per shift
                    self.schedule[day][shift].append(emp.name)
                    employee_shifts[emp.name] += 1
        
        self.display_schedule()
    
    def display_schedule(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        for day, shifts in self.schedule.items():
            self.output_text.insert(tk.END, f"{day}\n")
            for shift, employees in shifts.items():
                self.output_text.insert(tk.END, f"  {shift}: {', '.join(employees)}\n")
            self.output_text.insert(tk.END, "\n")
        self.output_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeScheduler(root)
    root.mainloop()
