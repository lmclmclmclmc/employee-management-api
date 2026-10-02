from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from database import (
    create_employee as create_employee_in_db,
    initialize_database,
    list_employees as list_employees_from_db,
    get_employee as get_employee_from_db,
    update_employee as update_employee_in_db,
    delete_employee as delete_employee_from_db,
)

app = FastAPI()
initialize_database()

class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1)
    salary: float = Field(ge=0)

@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee_update: EmployeeCreate
):
    employee = update_employee_in_db(
        employee_id,
        employee_update.name,
        employee_update.salary
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    employee = delete_employee_from_db(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    employee = get_employee_from_db(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="employee not found"
        )

    return employee 

@app.post("/employees", status_code=201)
def create_employee(employee: EmployeeCreate):
    return create_employee_in_db(
        employee.name,
        employee.salary
    )

@app.get("/employees")
def list_employees():
    return list_employees_from_db()