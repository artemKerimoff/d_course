from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, Text
from sqlalchemy.orm import relationship
from ..database import Base

class MaterialRequisition(Base):
    __tablename__ = "material_requisitions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Основные реквизиты
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    warehouse_id = Column(String(255), nullable=False)  # склад-отправитель (хранится как текст)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)  # подразделение-получатель
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)  # МОЛ
    
    requisition_number = Column(String(50), nullable=False)
    requisition_date = Column(Date, nullable=False)
    
    # Основание
    production_order_id = Column(Integer, ForeignKey("production_orders.id"), nullable=True)
    purpose = Column(Text)  # цель использования
    
    # Статус
    status = Column(String(50), default="черновик")  # черновик, утвержден, выполнен
    
    # Подписи
    issued_by_id = Column(Integer, ForeignKey("employees.id"))
    received_by_id = Column(Integer, ForeignKey("employees.id"))
    
    # Связи
    organization = relationship("Organization")
    # warehouse stored as plain string now; remove ORM relationship
    department = relationship("Department")
    employee = relationship("Employee", foreign_keys=[employee_id])
    production_order = relationship("ProductionOrder")
    issued_by = relationship("Employee", foreign_keys=[issued_by_id])
    received_by = relationship("Employee", foreign_keys=[received_by_id])
    
    items = relationship("MaterialRequisitionItem", back_populates="requisition", cascade="all, delete-orphan")

class MaterialRequisitionItem(Base):
    __tablename__ = "material_requisition_items"
    
    id = Column(Integer, primary_key=True, index=True)
    requisition_id = Column(Integer, ForeignKey("material_requisitions.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    # Данные позиции
    product_name = Column(String(500), nullable=False)
    unit = Column(String(50), nullable=False)
    requested_quantity = Column(Numeric(10, 3), nullable=False)  # затребовано
    issued_quantity = Column(Numeric(10, 3), nullable=False)     # отпущено
    price = Column(Numeric(15, 2), nullable=False)  # учетная цена
    amount = Column(Numeric(15, 2), nullable=False)
    
    # Связи
    requisition = relationship("MaterialRequisition", back_populates="items")
    product = relationship("Product")