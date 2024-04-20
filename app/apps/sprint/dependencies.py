import typing as tp

from fastapi import Depends

from ...database import get_session
from .repository import SprintRepository
from ..employees.dependencies import get_user_lead
from ..employees.schemas import TeamLeadData
from .schemas import SprintTeamLead


def get_sprint_repo(session=Depends(get_session)) -> SprintRepository:
    repo = SprintRepository(async_session=session)
    yield repo


async def get_lead_with_sprint(lead: TeamLeadData = Depends(get_user_lead),
                               sprint_repo: SprintRepository = Depends(get_sprint_repo)) -> SprintTeamLead:
    sprint = await sprint_repo.get_active_sprint(lead.team_id)
    return SprintTeamLead(sprint=sprint, **lead.model_dump())


SprintRepo = tp.Annotated[SprintRepository, Depends(get_sprint_repo)]
UserLeadSprint = tp.Annotated[SprintTeamLead, Depends(get_lead_with_sprint)]
