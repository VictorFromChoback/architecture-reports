from sqlalchemy import Column, Integer, String

from ...core.orm import Base


class Employees(Base):
    __tablename__ = "Employees"

    id = Column(Integer, primary_key=True)
    username: str = Column(String(length=320), unique=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    role = Column(String(length=100), unique=False, nullable=False)


employees = Employees.__table__
