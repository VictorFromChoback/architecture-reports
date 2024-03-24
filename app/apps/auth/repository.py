from sqlalchemy import select, insert

from ...core import BaseRepository
from .orm import Employees
from .schemas import NewEmployee
from .jwt import get_hashed_password


class EmployeeRepository(BaseRepository):

    async def get_by_username(self, username: str) -> Employees | None:
        return (await self.execute(select(Employees).where(Employees.username == username))).scalar()

    async def add_employee(self, new_employee: NewEmployee) -> None:
        password_hash: str = get_hashed_password(new_employee.password)
        await self.execute(insert(Employees).values(username=new_employee.username,
                                                    hashed_password=password_hash,
                                                    role=new_employee.role))
