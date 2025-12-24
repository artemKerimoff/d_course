from __future__ import annotations
from sqlalchemy import Column, Integer, String, Date
from ..database import Base

class ProductionOrder(Base):
    __tablename__ = "production_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(100), nullable=False)
    order_date = Column(Date)
