from datetime import date

from sqlalchemy import insert, select
from sqlalchemy.orm import DeclarativeMeta

from ...core.repository import BaseRepository
from ..auth.orm import employees
from ..employees.orm import employees_tree
from .orm import DateReports, SprintReports, sprint_reports
from ...exceptions import DBObjectNotFoundError
from .schemas import SubordinatesReports


class ReportRepository(BaseRepository):

    async def new_date_report(self, employee: int, text: str):
        await self.execute(insert(DateReports).values(employee=employee, text=text, date=date.today()))

    async def get_report(self, employee: int, orm: DeclarativeMeta) -> str:
        report: orm | None = (await self.execute(select(orm)
                                                 .where(orm.employee == employee))).scalar()
        if report is None:
            raise DBObjectNotFoundError("There is no report for you")
        return report.text

    async def get_date_report(self, employee: int) -> str:
        report: DateReports | None = (await self.execute(select(DateReports)
                                                         .where(DateReports.employee == employee,
                                                                DateReports.date == date.today()))).scalar()
        if report is None:
            raise DBObjectNotFoundError("There is no report for you")
        return report.text

    async def get_sprint_report(self, employee: int, sprint: int) -> str:
        report: SprintReports | None = (await self.execute(select(SprintReports)
                                                           .where(SprintReports.employee == employee,
                                                                  SprintReports.sprint == sprint))).scalar()
        if report is None:
            raise DBObjectNotFoundError("There is no report for you")
        return report.text

    async def new_sprint_report(self, employee: int, sprint: int, text: str):
        await self.execute(insert(SprintReports).values(employee=employee, text=text, sprint=sprint))

    async def get_subbordinates_reports(self, employee: int, sprint: int) -> list[SubordinatesReports]:
        subs = await self.fetch_all(select(employees_tree.join(employees,
                                                               employees.c.id == employees_tree.c.subordinate)
                                                         .join(sprint_reports,
                                                               employees.c.id == sprint_reports.c.employee))
                                    .where(employees_tree.c.lead == employee,
                                           sprint_reports.c.sprint == sprint))
        return [SubordinatesReports(subordinate=sub["username"], text=sub["text"]) for sub in subs]
