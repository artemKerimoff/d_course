from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Основные реквизиты
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    invoice_number = Column(String(50), nullable=False)
    invoice_date = Column(Date, nullable=False)
    payment_due_date = Column(Date)
    
    # Финансовые данные
    total_without_vat = Column(Numeric(15, 2), nullable=False)
    vat_amount = Column(Numeric(15, 2), nullable=False)
    total_with_vat = Column(Numeric(15, 2), nullable=False)
    
    # Статусы
    is_paid = Column(Boolean, default=False)
    is_received = Column(Boolean, default=False)  # товар получен
    
    # Основание
    contract_number = Column(String(100))
    contract_date = Column(Date)
    
    # Связи
    organization = relationship("Organization", foreign_keys=[organization_id])
    supplier = relationship("Organization", foreign_keys=[supplier_id])
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")

class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    # Данные позиции
    product_name = Column(String(500), nullable=False)
    unit = Column(String(50), nullable=False)  # единица измерения
    quantity = Column(Numeric(10, 3), nullable=False)
    price = Column(Numeric(15, 2), nullable=False)
    
    # НДС
    vat_rate = Column(Numeric(5, 2), nullable=False)  # 20.00, 10.00, 0.00
    amount_without_vat = Column(Numeric(15, 2), nullable=False)
    vat_amount = Column(Numeric(15, 2), nullable=False)
    amount_with_vat = Column(Numeric(15, 2), nullable=False)
    
    # Связи
    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product")