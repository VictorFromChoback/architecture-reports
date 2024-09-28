from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import database_start_up, database_tear_down


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database_start_up()
    yield
    await database_tear_down()
