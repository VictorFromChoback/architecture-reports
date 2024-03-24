from sqlalchemy import Column, Integer, ForeignKey, String

from ...core.orm import Base


class EmployeesTree(Base):
    __tablename__ = "EmployeesTree"

    lead = Column(Integer, ForeignKey("Employees.id"), primary_key=True)
    subordinate = Column(Integer, ForeignKey("Employees.id"), primary_key=True)


class Teams(Base):
    __tablename__ = "Teams"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), unique=False, nullable=False)
    team_lead = Column(Integer, ForeignKey("Employees.id"))


employees_tree = EmployeesTree.__table__
teams = Teams.__table__
