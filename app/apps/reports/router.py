import typing as tp
from fastapi import APIRouter, status, HTTPException, Body

from ..auth.dependencies import CurrentUser
from .dependencies import ReportRepo
from ..sprint.dependencies import UserLeadSprint
from ...core import MESSAGE_OK
from ...exceptions import DBObjectNotFoundError
from .schemas import SubordinatesReports


router = APIRouter()


@router.post("/date", status_code=status.HTTP_201_CREATED)
async def new_date_report(text: tp.Annotated[str, Body(...)],
                          report_repo: ReportRepo,
                          current_user: CurrentUser):
    await report_repo.new_date_report(current_user.id, text)
    return MESSAGE_OK


@router.get("/date")
async def get_date_report(report_repo: ReportRepo,
                          current_user: CurrentUser):
    try:
        return await report_repo.get_date_report(current_user.id)
    except DBObjectNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post("/sprint", status_code=status.HTTP_201_CREATED)
async def new_sprint_report(text: tp.Annotated[str, Body(...)],
                            report_repo: ReportRepo,
                            current_user: CurrentUser,
                            lead: UserLeadSprint):
    if lead.sprint is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active sprints")
    await report_repo.new_sprint_report(current_user.id, lead.sprint, text)
    return MESSAGE_OK


@router.get("/sprint", response_model=str)
async def get_sprint_report(report_repo: ReportRepo,
                            current_user: CurrentUser,
                            lead: UserLeadSprint):
    if lead.sprint is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active sprints")
    return await report_repo.get_sprint_report(current_user.id, lead.sprint)


@router.get("/sprint/subbordinates", response_model=list[SubordinatesReports])
async def get_subbordinates_reports(report_repo: ReportRepo,
                                    current_user: CurrentUser,
                                    lead: UserLeadSprint):
    if lead.sprint is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active sprints")
    return await report_repo.get_subbordinates_reports(current_user.id, lead.sprint)
