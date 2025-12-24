from __future__ import annotations
from sqlalchemy import Column, Integer, String, Date
from ..database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    post = Column(String(200), nullable=False)               # должность (пока строкой; позже можно FK -> Position)
    passport_series = Column(String(10), nullable=False)
    passport_number = Column(String(20), nullable=False)
    passport_issued_by = Column(String(255), nullable=False)
    passport_date_of_issue = Column(Date, nullable=False)    # YYYY-MM-DD