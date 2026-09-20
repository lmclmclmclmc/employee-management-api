class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def calculate_tax(self):
        if self.salary <= 5000:
            return 0
        elif self.salary <= 10000:
            return (self.salary - 5000) * 0.1
        else:
            return 500 + (self.salary - 10000) * 0.2

    def after_tax_salary(self):
        return self.salary - self.calculate_tax()


employees = [
    Employee("wang", 4000),
    Employee("li", 8000),
    Employee("zhang", 12000),       
]

sorted_employees = sorted(
    employees,
    key=lambda employee: employee.salary,
    reverse=True
)

for employee in sorted_employees:
    tax = employee.calculate_tax()
    after_tax = employee.after_tax_salary()

    print(
        f"{employee.name}：税前 {employee.salary:.2f} 元，"
        f"税额 {tax:.2f} 元，"
        f"税后 {after_tax:.2f} 元"
    )


        