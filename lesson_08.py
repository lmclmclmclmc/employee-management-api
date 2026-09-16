import json

def calculate_tax(salary):
    if salary <= 5000:
        tax = 0
    elif salary <= 10000:
        tax = (salary - 5000) * 0.1
    else:
        tax = 500 + (salary - 10000) * 0.2
    
    return tax

def save_employees(employees):
     with open("employees.json", "w", encoding="utf-8") as file:
        json.dump(employees, file, ensure_ascii=False, indent=2)

def load_employees():
    with open("employees.json", "r", encoding="utf-8") as file:
        return json.load(file)

def show_employees(employees):
    for employee in employees:
        tax = calculate_tax(employee["salary"])
        salary = employee["salary"]
        after_tax = salary - tax
        name = employee["name"]

        print(
            f"{name}: before tax {salary:.2f}, "
            f"tax {tax:.2f}, after tax {after_tax:.2f} yuan"
        )

def main():
    employees = []
    while True:
        name = input("请输入姓名，输入 q 结束：")
    
        if name.lower() == "q":
            if len(employees) < 2:
                print("请至少录入两名员工。")
                continue
            break

        while True:
            salary_text = input("请输入工资：")

            try:
                salary = float(salary_text)
            
            except ValueError:
                print("输入错误，工资必须是数字，请重新输入。")
                continue

            if salary < 0:
                print("工资不能是负数，请重新输入。")
                continue
            break

        employees.append({
            "name": name,
            "salary": salary
        })

    save_employees(employees)

    saved_employees = load_employees()

    show_employees(saved_employees)

if __name__ == "__main__":
    main()


       



        