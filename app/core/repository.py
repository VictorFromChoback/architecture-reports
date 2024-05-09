from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import CursorResult
from sqlalchemy.sql import Executable, Select
from sqlalchemy.orm import DeclarativeMeta


class BaseRepository:
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def execute(self, query: Executable) -> CursorResult:
        return await self.async_session.execute(query)

    async def fetch_objects(self, query: Select) -> list[DeclarativeMeta]:
        return [obj[0] for obj in (await self.execute(query)).fetchall()]

    async def fetch_all(self, query: Select) -> list[dict]:
        result = await self.execute(query)
        result = result.fetchall()
        return [row._asdict() for row in result]

    async def fetch_scalar(self, query: Select) -> DeclarativeMeta | None:
        return (await self.execute(query)).scalar()
