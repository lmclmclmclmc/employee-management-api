from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Employee


def get_employee_by_id(
    session: Session,
    employee_id: int,
) -> Employee | None:
    return session.get(Employee, employee_id)


def list_employees(
    session: Session,
    limit: int = 10,
    offset: int = 0,
    name: str | None = None,
) -> list[Employee]:
    statement = select(Employee)

    if name is not None:
        statement = statement.where(Employee.name.ilike(f"%{name}%"))

    statement = statement.order_by(Employee.id).limit(limit).offset(offset)

    return list(session.scalars(statement).all())


def create_employee(
    session: Session,
    name: str,
    department: str,
    salary: float,
) -> Employee:
    employee = Employee(
        name=name,
        department=department,
        salary=salary,
    )

    session.add(employee)
    session.commit()
    session.refresh(employee)

    return employee


def update_employee(
    session: Session,
    employee_id: int,
    name: str,
    department: str,
    salary: float,
) -> Employee | None:
    employee = session.get(Employee, employee_id)

    if employee is None:
        return None

    employee.name = name
    employee.department = department
    employee.salary = salary

    session.commit()
    session.refresh(employee)

    return employee


def delete_employee(
    session: Session,
    employee_id: int,
) -> Employee | None:
    employee = session.get(Employee, employee_id)

    if employee is None:
        return None

    session.delete(employee)
    session.commit()

    return employee
