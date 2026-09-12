def calculate_tax(salary):
    if salary <= 5000:
        tax = 0
    elif salary <= 10000:
        tax = (salary - 5000) * 0.1
    else:
        tax = 500 + (salary - 10000) * 0.2

    return tax

employees = [
    {"name":"xiao wang","salary": 4000},
    {"name":"xiao li","salary": 8000},
    {"name":"xiao zhang","salary": 12000}
]

for employ in employees:
    tax = calculate_tax(employ["salary"])
    salay = employ["salary"]
    after_tax = salay - tax
    name = employ["name"]

    print(f"{name}: before tax {salay:.2f},tax {tax:.2f},after tax {after_tax:.2f} yuan")