from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship
from ..database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    
    # Основные реквизиты
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    
    order_date = Column(Date, nullable=False)
    order_number = Column(String(50), nullable=False)
    purpose = Column(String(500))  # основание/цель
    
    # Связи
    organization = relationship("Organization")
    department = relationship("Department")
    employee = relationship("Employee")
    
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2))  # цена на момент выдачи
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product")