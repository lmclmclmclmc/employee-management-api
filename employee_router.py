from fastapi import APIRouter, Depends, HTTPException, Query

from database import (
    create_employee as create_employee_in_db,
)
from database import (
    delete_employee as delete_employee_from_db,
)
from database import (
    get_employee as get_employee_from_db,
)
from database import (
    list_employees as list_employees_from_db,
)
from database import (
    update_employee as update_employee_in_db,
)
from dependencies import get_current_username
from schemas import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
)

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
)


@router.get("", response_model=list[EmployeeResponse])
def list_employees(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    name: str | None = Query(default=None, min_length=1),
):
    return list_employees_from_db(limit, offset, name)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int):
    employee = get_employee_from_db(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return employee


@router.post(
    "",
    status_code=201,
    response_model=EmployeeResponse,
    dependencies=[Depends(get_current_username)],
)
def create_employee(employee: EmployeeCreate):
    return create_employee_in_db(
        employee.name,
        employee.salary,
    )


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
    dependencies=[Depends(get_current_username)],
)
def update_employee(
    employee_id: int,
    employee_update: EmployeeCreate,
):
    employee = update_employee_in_db(
        employee_id,
        employee_update.name,
        employee_update.salary,
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return employee


@router.patch(
    "/{employee_id}",
    response_model=EmployeeResponse,
    dependencies=[Depends(get_current_username)],
)
def partially_update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
):
    current_employee = get_employee_from_db(employee_id)

    if current_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    update_data = employee_update.model_dump(
        exclude_none=True,
    )

    new_name = update_data.get(
        "name",
        current_employee["name"],
    )
    new_salary = update_data.get(
        "salary",
        current_employee["salary"],
    )

    return update_employee_in_db(
        employee_id,
        new_name,
        new_salary,
    )


@router.delete(
    "/{employee_id}",
    response_model=EmployeeResponse,
    dependencies=[Depends(get_current_username)],
)
def delete_employee(employee_id: int):
    employee = delete_employee_from_db(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return employee
