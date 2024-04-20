from datetime import datetime

from pydantic import BaseModel
from enum import IntEnum


class TaskStatus(IntEnum):
    BACKLOG = 0
    INPROGRESS = 1
    REVIEW = 2
    FINISHED = 3


class NewTaskModel(BaseModel):
    name: str
    description: str
    employee: int | None = None
    sprint: int | None = None


class TaskComment(BaseModel):
    comment: str
    task: int


class Comment(BaseModel):
    author: str
    text: str
    creation_date: datetime
