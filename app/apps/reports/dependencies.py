import typing as tp

from fastapi import Depends

from ...database import get_session
from .repository import ReportRepository


def get_reports_repo(session=Depends(get_session)) -> ReportRepository:
    repo = ReportRepository(async_session=session)
    yield repo


ReportRepo = tp.Annotated[ReportRepository, Depends(get_reports_repo)]
