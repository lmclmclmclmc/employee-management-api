from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db_session import get_db
from dependencies import get_current_username
from employee_repository import (
    create_employee as create_employee_in_repository,
)
from employee_repository import (
    delete_employee as delete_employee_from_repository,
)
from employee_repository import (
    get_employee_by_id as get_employee_from_repository,
)
from employee_repository import (
    list_employees as list_employees_from_repository,
)
from employee_repository import (
    update_employee as update_employee_in_repository,
)
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
    session: Session = Depends(get_db),
):
    return list_employees_from_repository(
        session,
        limit=limit,
        offset=offset,
        name=name,
    )


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    session: Session = Depends(get_db),
):
    employee = get_employee_from_repository(
        session,
        employee_id,
    )

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
def create_employee(
    employee: EmployeeCreate,
    session: Session = Depends(get_db),
):
    return create_employee_in_repository(
        session,
        employee.name,
        employee.department,
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
    session: Session = Depends(get_db),
):
    employee = update_employee_in_repository(
        session,
        employee_id,
        employee_update.name,
        employee_update.department,
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
    session: Session = Depends(get_db),
):
    current_employee = get_employee_from_repository(
        session,
        employee_id,
    )

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
        current_employee.name,
    )
    new_department = update_data.get(
        "department",
        current_employee.department,
    )
    new_salary = update_data.get(
        "salary",
        current_employee.salary,
    )

    return update_employee_in_repository(
        session,
        employee_id,
        new_name,
        new_department,
        new_salary,
    )


@router.delete(
    "/{employee_id}",
    response_model=EmployeeResponse,
    dependencies=[Depends(get_current_username)],
)
def delete_employee(
    employee_id: int,
    session: Session = Depends(get_db),
):
    employee = delete_employee_from_repository(
        session,
        employee_id,
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return employee
