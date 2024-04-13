from sqlalchemy import Column, Integer, String, Date, ForeignKey

from ...core.orm import Base


class SprintReports(Base):
    __tablename__ = "SprintReports"

    sprint = Column(Integer, ForeignKey("Sprints.id"), primary_key=True)
    employee = Column(Integer, ForeignKey("Employees.id"), primary_key=True)
    text = Column(String, nullable=False, unique=False)


class DateReports(Base):
    __tablename__ = "DateReports"

    id = Column(Integer, primary_key=True)
    employee = Column(Integer, ForeignKey("Employees.id"))
    text = Column(String, nullable=False, unique=False)
    date = Column(Date, unique=False, nullable=False)


sprint_reports = SprintReports.__table__
date_reports = DateReports.__table__
