from __future__ import annotations
from datetime import date
from typing import List
from decimal import Decimal
from .common import OrmBase

class OrderItemBase(OrmBase):
    product_id: int
    amount: int
    price: Decimal = None

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int

class OrderBase(OrmBase):
    organization_id: int
    department_id: int
    employee_id: int
    order_date: date
    order_number: str
    purpose: str = ""

class OrderCreate(OrderBase):
    items: List[OrderItemCreate] = []

class OrderUpdate(OrderBase):
    items: List[OrderItemCreate] = []

class Order(OrderBase):
    id: int
    items: List[OrderItem] = []