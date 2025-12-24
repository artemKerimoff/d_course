from __future__ import annotations
from datetime import date
from typing import List, Optional
from decimal import Decimal
from .common import OrmBase

class InvoiceItemBase(OrmBase):
    product_id: int
    product_name: str
    unit: str
    quantity: Decimal
    price: Decimal
    vat_rate: Decimal
    amount_without_vat: Decimal
    vat_amount: Decimal
    amount_with_vat: Decimal

class InvoiceItemCreate(InvoiceItemBase):
    pass

class InvoiceItem(InvoiceItemBase):
    id: int
    invoice_id: int

class InvoiceBase(OrmBase):
    organization_id: int
    supplier_id: int
    invoice_number: str
    invoice_date: date
    payment_due_date: Optional[date] = None
    total_without_vat: Decimal
    vat_amount: Decimal
    total_with_vat: Decimal
    contract_number: Optional[str] = None
    contract_date: Optional[date] = None
    is_paid: bool = False
    is_received: bool = False

class InvoiceCreate(InvoiceBase):
    items: List[InvoiceItemCreate] = []

class InvoiceUpdate(InvoiceBase):
    items: List[InvoiceItemCreate] = []

class Invoice(InvoiceBase):
    id: int
    items: List[InvoiceItem] = []
    
    class Config:
        orm_mode = True