from pydantic import BaseModel

from ..auth.schemas import EmployeeData


class LeadSubordinate(BaseModel):
    lead: str
    subordinate: str


class TeamLeadData(EmployeeData):
    team_id: int
    team_name: str
