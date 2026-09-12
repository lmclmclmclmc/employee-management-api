"""第一课：变量、输入、数字转换和输出。"""

# 请运行程序，并根据提示输入信息。
name = input("请输入姓名：")
hours_per_day = float(input("每天工作多少小时："))
hourly_wage = float(input("每小时工资："))
workdays = int(input("每月工作多少天："))
monthly_reward = float(input("每月奖金："))

monthly_salary = hours_per_day * hourly_wage * workdays + monthly_reward


print(f"税前月薪：{monthly_salary:.2f} 元")

if 10000 >= monthly_salary > 5000:
    tax = (monthly_salary - 5000) * 0.1
elif monthly_salary > 10000:
    tax = 500 + (monthly_salary - 10000) * 0.2
else:
    tax = 0

after_tax_salary = monthly_salary - tax

print(f"预计税额：{tax:.2f} 元")

print(f"税后月薪：{after_tax_salary:.2f} 元")

