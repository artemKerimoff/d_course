from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..templating import get_templates
from ..crud import order as crud_order
from ..crud import organization as crud_org
from ..crud import employee as crud_emp
from ..crud import department as crud_dep
from ..crud import product as crud_prod
from ..schemas.orders import OrderCreate, OrderUpdate, OrderItemCreate

templates = get_templates()
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def list_orders(request: Request, db: Session = Depends(get_db)):
    items = crud_order.get_orders(db)
    return templates.TemplateResponse("orders/list.html", {"request": request, "orders": items})

@router.get("/create", response_class=HTMLResponse)
def create_order_form(request: Request, db: Session = Depends(get_db)):
    orgs = crud_org.get_organizations(db)
    deps = crud_dep.get_departments(db)
    emps = crud_emp.get_employees(db)
    prods = crud_prod.get_products(db)
    return templates.TemplateResponse(
        "orders/create.html",
        {"request": request, "orgs": orgs, "deps": deps, "emps": emps, "prods": prods}
    )

@router.post("/create")
def create_order(
    organization_id: int = Form(...),
    department_id: int = Form(...),
    employee_id: int = Form(...),
    order_date: str = Form(...),
    order_number: str = Form(...),
    purpose: str = Form(""),
    product_id: List[int] = Form([]),
    amount: List[int] = Form([]),
    db: Session = Depends(get_db),
):
    items = []
    for pid, qty in zip(product_id, amount):
        if str(pid).strip() == "" or str(qty).strip() == "":
            continue
        items.append(OrderItemCreate(product_id=int(pid), amount=int(qty)))

    obj_in = OrderCreate(
        organization_id=organization_id,
        department_id=department_id,
        employee_id=employee_id,
        order_date=order_date,
        order_number=order_number,
        purpose=purpose,
        items=items,
    )
    crud_order.create_order(db, obj_in)
    return RedirectResponse(url="/orders", status_code=303)

@router.get("/{order_id}", response_class=HTMLResponse)
def order_detail(order_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_order.get_order(db, order_id)
    return templates.TemplateResponse("orders/view.html", {"request": request, "order": item})

@router.get("/{order_id}/edit", response_class=HTMLResponse)
def edit_order_form(order_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_order.get_order(db, order_id)
    orgs = crud_org.get_organizations(db)
    deps = crud_dep.get_departments(db)
    emps = crud_emp.get_employees(db)
    prods = crud_prod.get_products(db)
    return templates.TemplateResponse(
        "orders/edit.html",
        {"request": request, "order": item, "orgs": orgs, "deps": deps, "emps": emps, "prods": prods}
    )

@router.post("/{order_id}/edit")
def update_order(
    order_id: int,
    organization_id: int = Form(...),
    department_id: int = Form(...),
    employee_id: int = Form(...),
    order_date: str = Form(...),
    order_number: str = Form(...),
    purpose: str = Form(""),
    product_id: List[int] = Form([]),
    amount: List[int] = Form([]),
    db: Session = Depends(get_db),
):
    items = []
    for pid, qty in zip(product_id, amount):
        if str(pid).strip() == "" or str(qty).strip() == "":
            continue
        items.append(OrderItemCreate(product_id=int(pid), amount=int(qty)))

    obj_in = OrderUpdate(
        organization_id=organization_id,
        department_id=department_id,
        employee_id=employee_id,
        order_date=order_date,
        order_number=order_number,
        purpose=purpose,
        items=items,
    )
    db_obj = crud_order.get_order(db, order_id)
    crud_order.update_order(db, db_obj, obj_in)
    return RedirectResponse(url="/orders", status_code=303)

@router.get("/{order_id}/print", response_class=HTMLResponse)
def order_print(order_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_order.get_order(db, order_id)
    return templates.TemplateResponse("orders/print.html", {"request": request, "order": item})

@router.get("/{order_id}/delete", response_class=HTMLResponse)
def delete_order_form(order_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_order.get_order(db, order_id)
    return templates.TemplateResponse("orders/delete.html", {"request": request, "order": item})

@router.post("/{order_id}/delete")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_obj = crud_order.get_order(db, order_id)
    crud_order.delete_order(db, db_obj)
    return RedirectResponse(url="/orders", status_code=303)