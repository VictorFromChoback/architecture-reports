from fastapi import APIRouter, status, HTTPException

from ..auth.dependencies import CurrentAdmin, EmployeeRepo, CurrentUser
from ..auth.schemas import NewEmployee
from .dependencies import EmployeesOrganizationRepo
from .schemas import LeadSubordinate, Employee
from ...core import MESSAGE_OK
from ...exceptions import DBObjectNotFoundError


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def new_employee(new_employee: NewEmployee,
                       employee_repo: EmployeeRepo,
                       _: CurrentAdmin):
    await employee_repo.add_employee(new_employee)
    return MESSAGE_OK


@router.get("", response_model=list[Employee])
async def get_employees(employee_repo: EmployeeRepo, _: CurrentUser):
    return await employee_repo.get_all_employees()


@router.post("/subordinate")
async def add_subordinate(lead_subordinate: LeadSubordinate,
                          organization_repo: EmployeesOrganizationRepo,
                          _: CurrentAdmin):
    try:
        await organization_repo.add_lead_subordinate(lead_subordinate)
    except DBObjectNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    return MESSAGE_OK


@router.post("/team")
async def create_team(name: str,
                      lead: int,
                      organization_repo: EmployeesOrganizationRepo,
                      _: CurrentAdmin):
    await organization_repo.create_team(lead, name)
    return MESSAGE_OK
