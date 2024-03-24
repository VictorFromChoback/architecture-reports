from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import CursorResult
from sqlalchemy.sql import Executable


class BaseRepository:
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def execute(self, query: Executable) -> CursorResult:
        return await self.async_session.execute(query)
