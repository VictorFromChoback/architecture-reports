import typing as tp

from fastapi import Depends

from ...database import get_session
from .repository import TaskRepository


def get_task_repo(session=Depends(get_session)) -> TaskRepository:
    repo = TaskRepository(async_session=session)
    yield repo


TaskRepo = tp.Annotated[TaskRepository, Depends(get_task_repo)]
