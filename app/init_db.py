from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from app.apps.auth.jwt import get_hashed_password
from app.apps.auth.orm import Employees
from app.database.meta import sync_engine_migrations


def init_users():
    password: str = "password"
    hashed_password = get_hashed_password(password)
    values = [
        {
            "id": 1,
            "username": "admin",
            "hashed_password": hashed_password,
            "role": "admin",
        },
    ]
    with sessionmaker(sync_engine_migrations)() as session:
        for value in values:
            query = insert(Employees).values(**value)
            try:
                session.execute(query)
                session.commit()
            except Exception as err:
                print("We got error", err)


def update_explicit_ids():
    TABLES = (
        "Employees",
    )
    try:
        with sessionmaker(sync_engine_migrations)() as session:
            for table in TABLES:
                session.execute(text(f"""SELECT setval('"{table}_id_seq"', (SELECT MAX(id) FROM "{table}"))"""))
    except Exception as err:
        print("We got error in explicit ids", err)


def main():
    init_users()
    update_explicit_ids()


if __name__ == '__main__':
    main()
