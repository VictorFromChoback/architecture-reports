from datetime import date

from sqlalchemy import insert, select, update

from ...exceptions import DBObjectNotFoundError
from ...core.repository import BaseRepository
from .orm import Sprints


class SprintRepository(BaseRepository):

    async def new_sprint(self, name: str, team: int, begin: date, end: date):
        await self.execute(insert(Sprints).values(name=name, begin=begin, end=end, team=team))

    async def update_sprint(self, sprint_id: int, team_id: int,
                            name: str | None, begin: date | None, end: date | None) -> None:
        data = {"id": sprint_id}
        if name:
            data["name"] = name
        if begin:
            data["begin"] = begin
        if end:
            data["end"] = end
        if not await self.fetch_scalar(select(Sprints)
                                       .where(Sprints.id == sprint_id, Sprints.team == team_id)):
            raise DBObjectNotFoundError("This is not your sprint")
        await self.execute(update(Sprints).where(Sprints.id == sprint_id).values(**data))

    async def get_sprints(self) -> list[Sprints]:
        return await self.fetch_objects(select(Sprints))

    async def get_active_sprint(self, team: int) -> int | None:
        sprint: Sprints | None = (await self.execute(select(Sprints).where(Sprints.team == team,
                                                                           Sprints.begin <= date.today(),
                                                                           Sprints.end >= date.today()))).scalar()
        if sprint is None:
            return None
        return sprint.id

    async def get_sprint(self, sprint_id: int) -> Sprints:
        return await self.fetch_scalar(select(Sprints).where(Sprints.id == sprint_id))
