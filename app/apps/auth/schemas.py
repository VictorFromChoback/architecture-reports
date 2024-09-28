from pydantic import BaseModel
from enum import StrEnum


class ResponseAuth(BaseModel):
    username: str
    role: str
    access_token: str
    token_type: str


class EmployeeData(BaseModel):
    id: int
    username: str
    role: str


class Roles(StrEnum):
    ADMIN = "admin"
    PROGRAMMER = "programmer"


class NewEmployee(BaseModel):
    username: str
    password: str
    role: str = Roles.PROGRAMMER
