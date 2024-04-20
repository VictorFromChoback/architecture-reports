from datetime import date

from fastapi import APIRouter, status

from ..employees.dependencies import CurrentLead
from ..auth.dependencies import CurrentUser
from .dependencies import SprintRepo
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


@router.get("", response_model=list[SprintModel])
async def get_sprints(sprint_repo: SprintRepo, _: CurrentUser):
    return await sprint_repo.get_sprints()
