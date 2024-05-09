from datetime import date

from fastapi import APIRouter, status, HTTPException

from ...exceptions import DBObjectNotFoundError
from ..employees.dependencies import CurrentLead
from ..auth.dependencies import CurrentUser
from .dependencies import SprintRepo, UserLeadSprint
from .schemas import SprintModel
from ...core import MESSAGE_OK


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def new_sprint(name: str,
                     begin: date,
                     end: date,
                     sprint_repo: SprintRepo,
                     lead: CurrentLead):
    await sprint_repo.new_sprint(name=name, team=lead.team_id, begin=begin, end=end)
    return MESSAGE_OK


@router.put("")
async def update_sprint(sprint_repo: SprintRepo,
                        lead: CurrentLead,
                        sprint: int,
                        name: str | None = None,
                        begin: date | None = None,
                        end: date | None = None):
    try:
        await sprint_repo.update_sprint(sprint_id=sprint, team_id=lead.team_id, name=name, begin=begin, end=end)
    except DBObjectNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    return MESSAGE_OK


@router.get("", response_model=list[SprintModel])
async def get_sprints(sprint_repo: SprintRepo, _: CurrentUser):
    return await sprint_repo.get_sprints()


@router.get("/active", response_model=SprintModel)
async def get_active_sprints(sprint_repo: SprintRepo, user: UserLeadSprint):
    """Returns active sprint for employee"""
    if user.sprint is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No active sprint for user you")
    return await sprint_repo.get_sprint(user.sprint)
