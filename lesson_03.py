def calculate_tax(salary):
    if salary <= 5000:
        tax = 0
    elif salary <= 10000:
        tax = (salary - 5000) * 0.1
    else:
        tax = 500 + (salary - 10000) * 0.2

    return tax

salaries = [4000,8000,12000,15000]

for salary in salaries:
    tax = calculate_tax(salary)
    after_tax = salary - tax

    print(f"税前:{salary:.2f} 元,税额:{tax:.2f} 元,税后:{after_tax:.2f} 元")

total_salay = sum(salaries)
average_salary = total_salay/len(salaries)

print(f"total salary:{total_salay:.2f},average salary:{average_salary:.2f}")