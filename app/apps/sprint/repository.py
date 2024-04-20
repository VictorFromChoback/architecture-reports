from datetime import date

from sqlalchemy import insert, select

from ...core.repository import BaseRepository
from .orm import Sprints
from .schemas import SprintModel


class SprintRepository(BaseRepository):

    async def new_sprint(self, name: str, team: int, begin: date, end: date):
        await self.execute(insert(Sprints).values(name=name, begin=begin, end=end, team=team))

    async def get_sprints(self) -> list[SprintModel]:
        await self.fetch_objects(select(Sprints))

    async def get_active_sprint(self, team: int) -> int | None:
        sprint: Sprints | None = (await self.execute(select(Sprints).where(Sprints.team == team,
                                                                           Sprints.begin <= date.today(),
                                                                           Sprints.end >= date.today()))).scalar()
        if sprint is None:
            return None
        return sprint.id
