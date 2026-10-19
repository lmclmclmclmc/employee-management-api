import sqlite3

from config import DATABASE_NAME


def initialize_database():
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                salary REAL NOT NULL CHECK (salary >= 0)
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)


def create_user(username, password_hash):
    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.execute(
                """
                INSERT INTO users (username, password_hash)
                VALUES (?,?)
                """,
                (username, password_hash),
            )

            return {
                "id": cursor.lastrowid,
                "username": username,
                "password_hash": password_hash,
            }

    except sqlite3.IntegrityError:
        return None


def get_user_by_username(username):
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.row_factory = sqlite3.Row

        row = connection.execute(
            """
            SELECT id, username, password_hash
            FROM users
            WHERE username = ?

            """,
            (username,),
        ).fetchone()

        if row is None:
            return None

        return dict(row)


def check_database_connection():
    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            connection.execute("SELECT 1")
        return True
    except sqlite3.Error:
        return False


def update_employee(employee_id, name, salary):
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.execute(
            """
            UPDATE employees
            SET name = ?, salary = ?
            WHERE id = ?
            """,
            (
                name,
                salary,
                employee_id,
            ),
        )

        if cursor.rowcount == 0:
            return None

    return get_employee(employee_id)


def delete_employee(employee_id):
    employee = get_employee(employee_id)

    if employee is None:
        return None

    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.execute("DELETE FROM employees WHERE id = ?", (employee_id,))

    return employee


def create_employee(name, salary):
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.execute(
            "INSERT INTO employees (name, salary) VALUES (?, ?)", (name, salary)
        )

        return {"id": cursor.lastrowid, "name": name, "salary": salary}


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
            (limit, offset),
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
            (employee_id,),
        ).fetchone()

        if row is None:
            return None

        return dict(row)


if __name__ == "__main__":
    initialize_database()
    created_employee = create_employee("wang", 8000)

    print(created_employee)
    print(list_employees())
