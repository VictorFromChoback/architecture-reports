from sqlalchemy import insert, select

from ..auth.repository import EmployeeRepository
from ..auth.repository import Employees
from .orm import EmployeesTree, Teams
from .schemas import LeadSubordinate
from ...exceptions import DBObjectNotFoundError


class EmployeesOrganizationRepository(EmployeeRepository):

    async def add_lead_subordinate(self, lead_subordinate: LeadSubordinate) -> None:
        subordinate = await self.get_by_username(lead_subordinate.subordinate)
        lead = await self.get_by_username(lead_subordinate.lead)
        if subordinate is None or lead is None:
            raise DBObjectNotFoundError("Incorrect employees")
        await self.execute(insert(EmployeesTree).values(lead=lead.id, subordinate=subordinate.id))

    async def create_team(self, lead: int, name: str):
        await self.execute(insert(Teams).values(name=name, team_lead=lead))

    async def find_team(self, employee: int) -> Teams:
        team: Teams | None = (await self.execute(select(Teams).where(Teams.team_lead == employee))).scalar()
        if team is None:
            raise DBObjectNotFoundError(f"User employee {employee} is not a team lead")
        return team

    async def find_lead(self, employee: int) -> Employees:
        while True:
            pair: EmployeesTree | None = (await self.execute(select(EmployeesTree)
                                                             .where(EmployeesTree.subordinate == employee))).scalar()
            if pair is None:
                break
            employee = pair.lead
        return (await self.execute(select(Employees).where(Employees.id == employee))).scalar()
