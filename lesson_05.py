employees = []

while True:
    name = input("请输入姓名，输入 q 结束：")

    if name == "q":
        break

    salary = float(input("请输入工资："))

    employees.append(
        {
            "name":name,
            "salary":salary
        }
    )

def calculate_tax(salary):
    if salary <= 5000:
        tax = 0
    elif salary <= 10000:
        tax = (salary - 5000) * 0.1
    else:
        tax = 500 + (salary - 10000) * 0.2

    return tax


for employ in employees:
    tax = calculate_tax(employ["salary"])
    salary = employ["salary"]
    after_tax = salary - tax
    name = employ["name"]

    print(f"{name}: before tax {salary:.2f},tax {tax:.2f},after tax {after_tax:.2f} yuan")