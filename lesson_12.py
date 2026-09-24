import sqlite3

DATABASE_NAME = "employees.db"

def add_employee(name, salary):
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.execute(
            "INSERT INTO employees (name, salary) VALUES (?, ?)",
            (name, salary)
        )

def update_salary(name, new_salary):
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.execute(
            "UPDATE employees SET salary = ? WHERE name = ?",
            (new_salary, name)
        )

def delete_employee(name):
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.execute(
            "DELETE FROM employees WHERE name = ?",
            (name,)
        )

def list_employees():
    with sqlite3.connect(DATABASE_NAME) as connection:
        return connection.execute(
            "SELECT name, salary FROM employees ORDER BY salary DESC"
        ).fetchall()

add_employee("zhao", 10000)

update_salary("zhao", 13000)

delete_employee("wang")

for name, salary in list_employees():
    print(f"{name}: {salary:.2f} yuan") 