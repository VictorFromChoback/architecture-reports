from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, text

from ...core.orm import Base


class Tasks(Base):
    __tablename__ = "Tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False, nullable=False)
    description = Column(String, unique=False, nullable=False)
    creation_datetime = Column(DateTime, unique=False, nullable=False)
    change_datetime = Column(DateTime, unique=False, nullable=False)
    employee = Column(Integer, ForeignKey("Employees.id"))
    sprint = Column(Integer, ForeignKey("Sprints.id"))
    status = Column(Integer, unique=False, nullable=False, server_default=text("0"))


class TaskComments(Base):
    __tablename__ = "TaskComments"

    id = Column(Integer, primary_key=True)
    task = Column(Integer, ForeignKey("Tasks.id"))
    author = Column(Integer, ForeignKey("Employees.id"))
    text = Column(String, nullable=False, unique=False)
    creation_date = Column(DateTime, unique=False, nullable=False)


tasks = Tasks.__table__
task_comments = TaskComments.__table__
