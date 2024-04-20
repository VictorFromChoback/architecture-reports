import typing as tp
from fastapi import APIRouter, status, HTTPException, Body

from ..auth.dependencies import CurrentUser
from .dependencies import ReportRepo
from ...core import MESSAGE_OK
from ...exceptions import DBObjectNotFoundError


router = APIRouter()


@router.post("/date", status_code=status.HTTP_201_CREATED)
async def new_date_report(text: tp.Annotated[str, Body(...)],
                          report_repo: ReportRepo,
                          current_user: CurrentUser):
    await report_repo.new_date_report(current_user.id, text)
    return MESSAGE_OK


@router.post("/sprint", status_code=status.HTTP_201_CREATED)
async def new_sprint_report(text: tp.Annotated[str, Body(...)],
                            report_repo: ReportRepo,
                            current_user: CurrentUser):
    await report_repo.new_date_report(current_user.id, text)
    return MESSAGE_OK
