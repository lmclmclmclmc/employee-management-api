import sqlite3

with sqlite3.connect("employees.db") as connection:
    row = connection.execute("""
        SELECT COUNT(*), AVG(salary), MIN(salary), MAX(salary)
        FROM employees
    """).fetchone()

    county = connection.execute(
        "SELECT COUNT(*) FROM employees WHERE salary >= ?", (8000,)
    ).fetchone()[0]

count, average, minimum, maximum = row  

print(f"count: {count}")
print(f"average: {average:.2f}")
print(f"min: {minimum:.2f}")
print(f"max: {maximum:.2f}")
print(f"more than 8000: {county}")