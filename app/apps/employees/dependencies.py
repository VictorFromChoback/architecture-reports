import typing as tp

from fastapi import Depends

from ...database import get_session
from .repository import EmployeesOrganizationRepository


def get_employee_organization_repo(session=Depends(get_session)) -> EmployeesOrganizationRepository:
    repo = EmployeesOrganizationRepository(async_session=session)
    yield repo


EmployeesOrganizationRepo = tp.Annotated[EmployeesOrganizationRepository,
                                         Depends(get_employee_organization_repo)]
