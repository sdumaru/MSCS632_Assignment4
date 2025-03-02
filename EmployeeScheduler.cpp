#include <iostream>
#include <vector>
#include <map>
#include <unordered_map>
#include <string>
#include <algorithm>
using namespace std;

// Define shift options
const vector<string> shifts = {"Morning", "Afternoon", "Evening"};
const vector<string> days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"};
const int max_shifts_per_week = 5;

// Mapping for user-friendly input
const unordered_map<char, string> shift_map = {{'N', "None"}, {'0', "None"}, {'M', "Morning"}, {'1', "Morning"}, {'A', "Afternoon"}, {'2', "Afternoon"}, {'E', "Evening"}, {'3', "Evening"}};

// Function to get shift input from user
pair<string, string> getShiftInput(const string &day)
{
    char p1, p2;
    cout << "Enter preferred shift 1 for " << day << " (N/0=None, M/1=Morning, A/2=Afternoon, E/3=Evening): ";
    cin >> p1;
    cin.ignore();
    cout << "Enter preferred shift 2 for " << day << " (N/0=None, M/1=Morning, A/2=Afternoon, E/3=Evening): ";
    cin >> p2;
    cin.ignore();
    return {shift_map.at(p1), shift_map.at(p2)};
}

// Employee class to store shift preferences and assigned shifts
class Employee
{
public:
    string name;
    unordered_map<string, pair<string, string>> preferences;
    unordered_map<string, string> assigned_shifts;
    int assigned_days = 0;

    Employee(string emp_name, unordered_map<string, pair<string, string>> prefs)
        : name(emp_name), preferences(prefs) {}
};

// Employee Scheduler class
class EmployeeScheduler
{
private:
    vector<Employee> employees;
    map<string, map<string, vector<string>>> schedule;

public:
    void addEmployee(const string &name, unordered_map<string, pair<string, string>> prefs)
    {
        employees.emplace_back(name, prefs);
    }

    void generateSchedule()
    {
        schedule.clear();
        for (auto &emp : employees)
        {
            emp.assigned_days = 0;
            emp.assigned_shifts.clear();
        }

        for (auto &emp : employees)
        {
            if (emp.assigned_days >= max_shifts_per_week)
                continue;

            for (const auto &day_pref : emp.preferences)
            {
                if (emp.assigned_days >= max_shifts_per_week)
                    break;

                string day = day_pref.first;
                string priority1 = day_pref.second.first;
                string priority2 = day_pref.second.second;

                if (priority1 == "None" && priority2 == "None")
                    continue;

                if (emp.assigned_shifts.find(day) == emp.assigned_shifts.end())
                {
                    vector<string> available_shifts;
                    if (priority1 != "None")
                        available_shifts.push_back(priority1);
                    if (priority2 != "None")
                        available_shifts.push_back(priority2);
                    bool assigned = false;

                    for (const auto &shift : available_shifts)
                    {
                        if (schedule[day][shift].size() < 2)
                        {
                            schedule[day][shift].push_back(emp.name);
                            emp.assigned_shifts[day] = shift;
                            emp.assigned_days++;
                            assigned = true;
                            break;
                        }
                    }
                }
            }
        }
    }

    void displaySchedule()
    {
        cout << "\nFinal Schedule:\n";
        for (const auto &day : days)
        {
            cout << day << "\n";
            for (const auto &shift : shifts)
            {
                cout << "  " << shift << ": ";
                if (schedule[day][shift].empty())
                {
                    cout << "No employees assigned";
                }
                else
                {
                    for (const auto &emp : schedule[day][shift])
                    {
                        cout << emp << ", ";
                    }
                }
                cout << "\n";
            }
            cout << "\n";
        }
    }
};

int main()
{
    EmployeeScheduler scheduler;
    int num_employees;
    cout << "Enter number of employees: ";
    cin >> num_employees;
    cin.ignore();

    for (int i = 0; i < num_employees; i++)
    {
        string name;
        cout << "\nEnter employee " << i + 1 << " name: ";
        cin >> name;
        cin.ignore();
        unordered_map<string, pair<string, string>> preferences;

        char reuse;
        cout << "Would you like to use the same shift preferences for all days? (Y/N): ";
        cin >> reuse;
        cin.ignore();

        if (reuse == 'Y' || reuse == 'y')
        {
            auto common_shifts = getShiftInput("all days");

            char modify;
            cout << "Do you want to modify preferences for specific days? (Y/N): ";
            cin >> modify;
            cin.ignore();

            if (modify == 'Y' || modify == 'y')
            {
                for (const auto &day : days)
                {
                    char mod_day;
                    cout << "Modify shift for " << day << "? (Y/N): ";
                    cin >> mod_day;
                    cin.ignore();
                    if (mod_day == 'Y' || mod_day == 'y')
                    {
                        preferences[day] = getShiftInput(day);
                    }
                    else
                    {
                        preferences[day] = common_shifts;
                    }
                }
            }
            else
            {
                for (const auto &day : days)
                {
                    preferences[day] = common_shifts;
                }
            }
        }
        scheduler.addEmployee(name, preferences);
    }

    scheduler.generateSchedule();
    scheduler.displaySchedule();
    return 0;
}
