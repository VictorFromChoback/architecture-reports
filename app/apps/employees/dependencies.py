import typing as tp

from fastapi import Depends, status, HTTPException

from ..auth.dependencies import get_current_user
from ..auth.schemas import EmployeeData
from .schemas import TeamLeadData
from ...database import get_session
from .repository import EmployeesOrganizationRepository
from ...exceptions import DBObjectNotFoundError


def get_employee_organization_repo(session=Depends(get_session)) -> EmployeesOrganizationRepository:
    repo = EmployeesOrganizationRepository(async_session=session)
    yield repo


EmployeesOrganizationRepo = tp.Annotated[EmployeesOrganizationRepository,
                                         Depends(get_employee_organization_repo)]


async def get_current_lead(
        current_user: EmployeeData = Depends(get_current_user),
        employee_repo: EmployeesOrganizationRepository = Depends(get_employee_organization_repo)
) -> TeamLeadData:
    try:
        team = await employee_repo.find_team(current_user.id)
    except DBObjectNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    return TeamLeadData(team_id=team.id, team_name=team.name, **current_user.model_dump())


async def get_user_lead(
        current_user: EmployeeData = Depends(get_current_user),
        employee_repo: EmployeesOrganizationRepository = Depends(get_employee_organization_repo)
) -> TeamLeadData:
    try:
        team_lead = await employee_repo.find_lead(current_user.id)
        team = await employee_repo.find_team(team_lead.id)
    except DBObjectNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    return TeamLeadData(team_id=team.id,
                        team_name=team.name,
                        role=team_lead.role,
                        id=team_lead.id,
                        username=team_lead.username)


CurrentLead = tp.Annotated[TeamLeadData, Depends(get_current_lead)]
