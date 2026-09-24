import sqlite3

DATABASE_NAME = "employees_unique.db"

with sqlite3.connect(DATABASE_NAME) as connection:
    connection.execute("""
        CREATE TABLE IF NOT EXISTS employees_unique (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            salary REAL NOT NULL
        )
    """)

def add_employee(name, salary):
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.execute("""
            INSERT INTO employees_unique (name, salary) VALUES (?, ?)
        """, (name, salary))

for _ in range(2):
    try:
        add_employee("zhao", 10000)
        print("add")
    except sqlite3.IntegrityError:
        print("falure")

def list_employee():
    with sqlite3.connect(DATABASE_NAME) as connection:
        return connection.execute(
            "SELECT name, salary FROM employees_unique ORDER BY salary DESC"
        ).fetchall()

print(list_employee())