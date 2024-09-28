from datetime import datetime

from pydantic import BaseModel
from enum import IntEnum


class TaskStatus(IntEnum):
    BACKLOG = 0
    INPROGRESS = 1
    REVIEW = 2
    FINISHED = 3


STATUS2ID = {"backlog": TaskStatus.BACKLOG,
             "inprogress": TaskStatus.INPROGRESS,
             "review": TaskStatus.REVIEW,
             "finished": TaskStatus.FINISHED}


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


class TasksFilterRequest(BaseModel):
    employee: int | None = None
    name_substr: str | None = None
    descr_substr: str | None = None
    status: int | None = None
    sprint: int | None = None


class TaskResponse(BaseModel):
    id: int
    name: str
    description: str
    creation_datetime: datetime
    change_datetime: datetime
    status: int
