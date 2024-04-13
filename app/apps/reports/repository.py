from datetime import date

from sqlalchemy import insert

from ...core.repository import BaseRepository
from .orm import DateReports, SprintReports


class ReportRepository(BaseRepository):

    async def new_date_report(self, employee: int, text: str):
        await self.execute(insert(DateReports).values(employee=employee, text=text, date=date.today()))

    async def new_sprint_report(self, employee: int, text: str):
        await self.execute(insert(SprintReports).values(employee=employee, text=text))
