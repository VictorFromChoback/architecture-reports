from pydantic import BaseModel


class SubordinatesReports(BaseModel):
    subordinate: str
    text: str
