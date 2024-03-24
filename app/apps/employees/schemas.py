from pydantic import BaseModel


class LeadSubordinate(BaseModel):
    lead: str
    subordinate: str
