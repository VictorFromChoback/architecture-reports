from alembic import command
from alembic.config import Config

from .meta import engine


async def disconnect_db():
    await engine.dispose()


async def migrate_alembic():
    # To preven logger override
    alembic_config = Config('/reports/alembic.ini')
    command.upgrade(alembic_config, 'head')


async def database_start_up():
    await migrate_alembic()


async def database_tear_down():
    await disconnect_db()
