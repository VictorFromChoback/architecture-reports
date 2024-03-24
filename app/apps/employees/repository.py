from sqlalchemy import insert

from ..auth.repository import EmployeeRepository
from .orm import EmployeesTree
from .schemas import LeadSubordinate
from ...exceptions import DBObjectNotFoundError


class EmployeesOrganizationRepository(EmployeeRepository):

    async def add_lead_subordinate(self, lead_subordinate: LeadSubordinate) -> None:
        subordinate = await self.get_by_username(lead_subordinate.subordinate)
        lead = await self.get_by_username(lead_subordinate.lead)
        if subordinate is None or lead is None:
            raise DBObjectNotFoundError("Incorrect employees")
        await self.execute(insert(EmployeesTree).values(lead=lead.id, subordinate=subordinate.id))
