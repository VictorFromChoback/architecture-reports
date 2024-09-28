from contextlib import asynccontextmanager

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from ..exceptions import DBObjectNotFoundError
from .meta import engine


def get_session_maker():
    '''
    Returns class of session
    '''
    return sessionmaker(engine, class_=AsyncSession)()


async def get_session():
    '''
    It is main dependency for Data Access Layer
    Dependencies which use repositories must use
    this function as Depends argument.
    >>> def get_repo(session = Depends(get_session))
    '''
    async with get_session_maker() as session:
        try:
            yield session
        except DBObjectNotFoundError as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise
        else:
            await session.commit()


get_session_manager = asynccontextmanager(get_session)
