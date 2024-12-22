from flask import Flask, render_template
import time
import random
import matplotlib.pyplot as plt
import io
import base64
app = Flask(__name__)
class Employee:
    def __init__(self, emp_id, name, age, salary, designation, mobile):
        self.emp_id = emp_id
        self.name = name
        self.age = age
        self.salary = salary
        self.designation = designation
        self.mobile = mobile
employees = [
    Employee(1, "Pratham", 45, 90000, "Manager", "9876543210"),
    Employee(2, "Divya", 25, 50000, "Developer", "9876543211"),
    Employee(3, "Nachiket", 22, 30000, "Intern", "9876543212"),
    Employee(4, "Dhruvil", 60, 150000, "CEO", "9876543213"),
    Employee(5, "Deepak", 35, 70000, "Designer", "9876543214"),
]
def linear_search(employees, target, key):
    for i, emp in enumerate(employees):
        if getattr(emp, key) == target:
            return i
    return -1
def binary_search_recursive(employees, target, key, low, high):
    if high >= low:
        mid = (high + low) // 2
        if getattr(employees[mid], key) == target:
            return mid
        elif getattr(employees[mid], key) > target:
            return binary_search_recursive(employees, target, key, low, mid - 1)
        else:
            return binary_search_recursive(employees, target, key, mid + 1, high)
    else:
        return -1

def measure_time(search_func, employees, target, key, *args):
    start_time = time.time()
    result = search_func(employees, target, key, *args)
    end_time = time.time()
    return result, end_time - start_time

@app.route('/')
def index():
    highest_salary = max(employees, key=lambda x: x.salary).salary
    index_high, linear_time_high = measure_time(linear_search, employees, highest_salary, "salary")
    highest_salary_designation = employees[index_high].designation

    lowest_salary = min(employees, key=lambda x: x.salary).salary
    index_low, linear_time_low = measure_time(linear_search, employees, lowest_salary, "salary")
    lowest_salary_name = employees[index_low].name

    youngest_age = min(employees, key=lambda x: x.age).age
    index_young, linear_time_young = measure_time(linear_search, employees, youngest_age, "age")
    youngest_mobile = employees[index_young].mobile

    oldest_age = max(employees, key=lambda x: x.age).age
    index_old, linear_time_old = measure_time(linear_search, employees, oldest_age, "age")
    oldest_salary = employees[index_old].salary

    sizes = [10, 100, 500, 1000, 5000, 10000]
    linear_times = []
    binary_times = []

    for size in sizes:
        sample_employees = random.sample(employees * (size // len(employees)), size)
        sample_employees.sort(key=lambda x: x.salary)
        target = sample_employees[-1].salary

        _, linear_time = measure_time(linear_search, sample_employees, target, "salary")
        _, binary_time = measure_time(binary_search_recursive, sample_employees, target, "salary", 0, len(sample_employees) - 1)
        linear_times.append(linear_time)
        binary_times.append(binary_time)
    plt.plot(sizes, linear_times, label="Linear Search")
    plt.plot(sizes, binary_times, label="Binary Search")
    plt.xlabel('Number of Elements')
    plt.ylabel('Time Taken (seconds)')
    plt.title('Time Taken vs Number of Elements')
    plt.legend()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('prac4.html',
                           plot_url=plot_url,
                           highest_salary_designation=highest_salary_designation,
                           lowest_salary_name=lowest_salary_name,
                           youngest_mobile=youngest_mobile,
                           oldest_salary=oldest_salary)
if __name__ == '__main__':
    app.run(debug=True)
