import sqlite3

connection = sqlite3.connect("employees.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        salary REAL NOT NULL
    )
""")

cursor.execute("DELETE FROM employees")

employees = [
    ("wang", 4000),
    ("li", 8000),
    ("zhang", 12000)
]

cursor.executemany(
    "INSERT INTO employees (name, salary) VALUES(?, ?)",
    employees
)

connection.commit()

cursor.execute("""
    SELECT name, salary
    FROM employees
    ORDER BY salary DESC
""")

rows = cursor.fetchall()

for name, salary in rows:
    print(f"{name}: {salary:.2f} yuan")

cursor.execute("""
    SELECT name, salary
    FROM employees
    WHERE salary >= ?
    ORDER BY salary DESC
""", (8000,))

high_salary_rows = cursor.fetchall()

print("not lower than 8000:")

for name, salary in high_salary_rows:
    print(f"{name}: {salary:.2f} yuan")



connection.close()
