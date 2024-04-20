from datetime import date

from pydantic import BaseModel


class SprintModel(BaseModel):
    name: str
    begin: date
    end: date
