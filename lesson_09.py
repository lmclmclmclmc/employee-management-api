employees = [
    {"name": "小王", "salary": 4000},
    {"name": "小李", "salary": 12000},
    {"name": "小张", "salary": 8000},
    {"name": "小赵", "salary": 15000},
]   

high_salary_names = [
    employee["name"]
    for employee in employees
    if employee["salary"] >= 10000
]

sorted_employees = sorted(
    employees,
    key=lambda employee: employee["salary"],
    reverse=True
)

sum_salary = 0

for sorted_employee in sorted_employees:
    print(f"{sorted_employee['name']}: {sorted_employee['salary']} yuan") 
    sum_salary += sorted_employee["salary"]

average_salary = sum_salary / len(sorted_employees)

print(f"平均工资：{average_salary:.2f} 元")

print(high_salary_names)
