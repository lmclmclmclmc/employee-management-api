from fastapi import FastAPI, HTTPException

from pydantic import BaseModel, Field

app = FastAPI()

class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1)
    salary: float = Field(ge=0)

employees = []

@app.get("/")
def read_root():
    return {"message": "Hello Python"}

@app.get("/employees/{employee_id}")
def read_employee(employee_id: int):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )

@app.post("/employees", status_code=201)
def create_employee(employee: EmployeeCreate):
    employee_data = employee.model_dump()
    employee_data["id"] = len(employees) + 1
    employees.append(employee_data)
    return employee_data

@app.get("/employees")
def list_employees():
    return employees

@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee_update: EmployeeCreate
):
    for employee in employees:
        if employee["id"] == employee_id:
            employee["name"] = employee_update.name
            employee["salary"] = employee_update.salary
            return employee

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    for index, employee in enumerate(employees):
        if employee["id"] == employee_id:
            deleted_employee = employees.pop(index)
            return deleted_employee

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )