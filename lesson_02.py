"""第四课：使用函数计算个人所得税。"""

# 请从这里开始写代码。
def calculate_tax(salary):
    if salary <= 5000:
        tax = 0
    elif salary <= 10000:
        tax = (salary - 5000) * 0.1
    else:
        tax = 500 + (salary - 10000) * 0.2

    return tax

user_salary = float(input("input user salary: "))

tax = calculate_tax(user_salary)

after_tax = user_salary - tax

print(f"user tax:{tax:.2f}")
print(f"user salary after tax:{after_tax:.2f}")
