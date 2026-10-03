from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from database import (
    create_employee as create_employee_in_db,
    initialize_database,
    list_employees as list_employees_from_db,
    get_employee as get_employee_from_db,
    update_employee as update_employee_in_db,
    delete_employee as delete_employee_from_db,
)

class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    salary: float | None = Field(default=None, ge=0)

class EmployeeResponse(BaseModel):
    id: int
    name: str
    salary: float

app = FastAPI()
initialize_database()



class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1)
    salary: float = Field(ge=0)


@app.patch("/employees/{employee_id}", response_model=EmployeeResponse)
def partially_update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate
):
    current_employee = get_employee_from_db(employee_id)

    if current_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not Found"
        )

    update_data = employee_update.model_dump(
        exclude_none=True
    )

    new_name = update_data.get(
        "name",
        current_employee["name"]
    )
    new_salary = update_data.get(
        "salary",
        current_employee["salary"]
    )

    return update_employee_in_db(
        employee_id,
        new_name,
        new_salary
    )

@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
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

@app.delete("/employees/{employee_id}", response_model=EmployeeResponse)
def delete_employee(employee_id: int):
    employee = delete_employee_from_db(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int):
    employee = get_employee_from_db(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="employee not found"
        )

    return employee 

@app.post("/employees", status_code=201, response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate):
    return create_employee_in_db(
        employee.name,
        employee.salary
    )

@app.get("/employees", response_model=list[EmployeeResponse])
def list_employees(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    return list_employees_from_db(limit, offset)


