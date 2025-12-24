from __future__ import annotations
from datetime import date
from typing import List, Optional
from decimal import Decimal
from .common import OrmBase

class MaterialRequisitionItemBase(OrmBase):
    product_id: int
    product_name: str
    unit: str
    requested_quantity: Decimal
    issued_quantity: Decimal
    price: Decimal
    amount: Decimal

class MaterialRequisitionItemCreate(MaterialRequisitionItemBase):
    pass

class MaterialRequisitionItem(MaterialRequisitionItemBase):
    id: int
    requisition_id: int

class MaterialRequisitionBase(OrmBase):
    organization_id: int
    warehouse_id: str
    department_id: int
    employee_id: int
    requisition_number: str
    requisition_date: date
    production_order_id: Optional[int] = None
    purpose: Optional[str] = None
    status: str = "черновик"
    issued_by_id: Optional[int] = None
    received_by_id: Optional[int] = None

class MaterialRequisitionCreate(MaterialRequisitionBase):
    items: List[MaterialRequisitionItemCreate] = []

class MaterialRequisitionUpdate(MaterialRequisitionBase):
    items: List[MaterialRequisitionItemCreate] = []

class MaterialRequisition(MaterialRequisitionBase):
    id: int
    items: List[MaterialRequisitionItem] = []
    
    class Config:
        orm_mode = True