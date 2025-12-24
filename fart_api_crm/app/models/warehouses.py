from __future__ import annotations
from sqlalchemy import Column, Integer, String
from ..database import Base

class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
