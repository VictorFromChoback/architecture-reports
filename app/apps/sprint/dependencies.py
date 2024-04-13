import typing as tp

from fastapi import Depends

from ...database import get_session
from .repository import SprintRepository


def get_sprint_repo(session=Depends(get_session)) -> SprintRepository:
    repo = SprintRepository(async_session=session)
    yield repo


SprintRepo = tp.Annotated[SprintRepository, Depends(get_sprint_repo)]
