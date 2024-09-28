from sqlalchemy import Column, Integer, String, Date, ForeignKey

from ...core.orm import Base


class Sprints(Base):
    __tablename__ = "Sprints"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False, nullable=False)
    team = Column(Integer, ForeignKey("Team.id"))
    begin = Column(Date, unique=False, nullable=False)
    end = Column(Date, unique=False, nullable=False)


sprints = Sprints.__table__
