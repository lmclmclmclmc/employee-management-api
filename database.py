import sqlite3
import os

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "api_employees.db"
)

def initialize_database():
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                salary REAL NOT NULL CHECK (salary >= 0)
            )
        """)

def update_employee(employee_id, name, salary):
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.execute(
            """
            UPDATE employees
            SET name = ?, salary = ?
            WHERE id = ?
            """,
            (name, salary, employee_id,)
        )

        if cursor.rowcount == 0:
            return None

    return get_employee(employee_id)

def delete_employee(employee_id):
    employee = get_employee(employee_id)

    if employee is None:
        return None

    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.execute(
            "DELETE FROM employees WHERE id = ?",
            (employee_id,)
        )

    return employee


def create_employee(name, salary):
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.execute(
            "INSERT INTO employees (name, salary) VALUES (?, ?)",
            (name, salary)
        )

        return {
            "id": cursor.lastrowid,
            "name": name,
            "salary": salary
        }

def list_employees(limit=10, offset=0):
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute(
            """
            SELECT id, name, salary 
            FROM employees 
            ORDER BY id
            LIMIT ? OFFSET ?
            """,
            (limit, offset)
        ).fetchall()

        return [dict(row) for row in rows]

def get_employee(employee_id):
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.row_factory = sqlite3.Row

        row = connection.execute(
            """
            SELECT id, name, salary
            FROM employees
            WHERE id = ?    
            """,
            (employee_id,)
        ).fetchone()

        if row is None:
            return None

        return dict(row)



if __name__ == "__main__":
    initialize_database()
    created_employee = create_employee("wang", 8000)

    print(created_employee)
    print(list_employees())