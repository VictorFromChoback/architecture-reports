from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

from ..configs import app_settings


def get_db_url(sync: bool = True) -> str:
    user_password: str = f"{app_settings.postgres.user}:{app_settings.postgres.password}"
    path: str = f"database:{app_settings.postgres.port}/{app_settings.postgres.db}"
    return f"postgresql{'' if sync else '+asyncpg'}://{user_password}@{path}"


engine = create_async_engine(get_db_url(sync=False), pool_size=5, echo=False)

# Engine for alembic migrations
sync_engine_migrations = create_engine(get_db_url())
