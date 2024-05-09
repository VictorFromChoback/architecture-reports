from datetime import date

from pydantic import BaseModel

from ..employees.schemas import TeamLeadData


class SprintModel(BaseModel):
    id: str
    name: str
    begin: date
    end: date


class SprintTeamLead(TeamLeadData):
    sprint: int | None
