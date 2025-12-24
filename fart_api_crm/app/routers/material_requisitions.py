from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..templating import get_templates
from ..crud import material_requisition as crud_requisition
from ..crud import organization as crud_org
from ..crud import employee as crud_emp
from ..crud import department as crud_dep
from ..crud import warehouse as crud_warehouse
from ..crud import product as crud_prod
from ..crud import production_order as crud_prod_order
from ..schemas.material_requisition import MaterialRequisitionCreate, MaterialRequisitionUpdate, MaterialRequisitionItemCreate

templates = get_templates()
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def list_requisitions(request: Request, db: Session = Depends(get_db)):
    items = crud_requisition.get_material_requisitions(db)
    return templates.TemplateResponse("requisitions/list.html", {"request": request, "requisitions": items})

@router.get("/create", response_class=HTMLResponse)
def create_requisition_form(request: Request, db: Session = Depends(get_db)):
    orgs = crud_org.get_organizations(db)
    warehouses = crud_warehouse.get_warehouses(db)
    deps = crud_dep.get_departments(db)
    emps = crud_emp.get_employees(db)
    prods = crud_prod.get_products(db)
    prod_orders = crud_prod_order.get_production_orders(db)
    return templates.TemplateResponse(
        "requisitions/create.html",
        {
            "request": request, 
            "orgs": orgs, 
            "warehouses": warehouses,
            "deps": deps, 
            "emps": emps, 
            "prods": prods,
            "prod_orders": prod_orders
        }
    )

@router.post("/create")
def create_requisition(
    organization_id: int = Form(...),
    warehouse_id: str = Form(...),
    department_id: int = Form(...),
    employee_id: int = Form(...),
    requisition_number: str = Form(...),
    requisition_date: str = Form(...),
    production_order_id: int = Form(None),
    purpose: str = Form(""),
    status: str = Form("черновик"),
    issued_by_id: int = Form(None),
    received_by_id: int = Form(None),
    product_id: List[int] = Form([]),
    product_name: List[str] = Form([]),
    unit: List[str] = Form([]),
    requested_quantity: List[float] = Form([]),
    issued_quantity: List[float] = Form([]),
    price: List[float] = Form([]),
    amount: List[float] = Form([]),
    db: Session = Depends(get_db),
):
    items = []
    for pid, pname, u, req_qty, iss_qty, pr, amt in zip(
        product_id, product_name, unit, requested_quantity, 
        issued_quantity, price, amount
    ):
        if str(pid).strip() == "":
            continue
        items.append(MaterialRequisitionItemCreate(
            product_id=int(pid),
            product_name=pname,
            unit=u,
            requested_quantity=req_qty,
            issued_quantity=iss_qty,
            price=pr,
            amount=amt,
        ))

    obj_in = MaterialRequisitionCreate(
        organization_id=organization_id,
        warehouse_id=warehouse_id,
        department_id=department_id,
        employee_id=employee_id,
        requisition_number=requisition_number,
        requisition_date=requisition_date,
        production_order_id=production_order_id if production_order_id else None,
        purpose=purpose if purpose else None,
        status=status,
        issued_by_id=issued_by_id if issued_by_id else None,
        received_by_id=received_by_id if received_by_id else None,
        items=items,
    )
    crud_requisition.create_material_requisition(db, obj_in)
    return RedirectResponse(url="/requisitions", status_code=303)

@router.get("/{requisition_id}", response_class=HTMLResponse)
def requisition_detail(requisition_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_requisition.get_material_requisition(db, requisition_id)
    return templates.TemplateResponse("requisitions/view.html", {"request": request, "requisition": item})

@router.get("/{requisition_id}/edit", response_class=HTMLResponse)
def edit_requisition_form(requisition_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_requisition.get_material_requisition(db, requisition_id)
    orgs = crud_org.get_organizations(db)
    warehouses = crud_warehouse.get_warehouses(db)
    deps = crud_dep.get_departments(db)
    emps = crud_emp.get_employees(db)
    prods = crud_prod.get_products(db)
    prod_orders = crud_prod_order.get_production_orders(db)
    return templates.TemplateResponse(
        "requisitions/edit.html",
        {
            "request": request, 
            "requisition": item,
            "orgs": orgs, 
            "warehouses": warehouses,
            "deps": deps, 
            "emps": emps, 
            "prods": prods,
            "prod_orders": prod_orders
        }
    )

@router.post("/{requisition_id}/edit")
def update_requisition(
    requisition_id: int,
    organization_id: int = Form(...),
    warehouse_id: str = Form(...),
    department_id: int = Form(...),
    employee_id: int = Form(...),
    requisition_number: str = Form(...),
    requisition_date: str = Form(...),
    production_order_id: int = Form(None),
    purpose: str = Form(""),
    status: str = Form("черновик"),
    issued_by_id: int = Form(None),
    received_by_id: int = Form(None),
    product_id: List[int] = Form([]),
    product_name: List[str] = Form([]),
    unit: List[str] = Form([]),
    requested_quantity: List[float] = Form([]),
    issued_quantity: List[float] = Form([]),
    price: List[float] = Form([]),
    amount: List[float] = Form([]),
    db: Session = Depends(get_db),
):
    items = []
    for pid, pname, u, req_qty, iss_qty, pr, amt in zip(
        product_id, product_name, unit, requested_quantity, 
        issued_quantity, price, amount
    ):
        if str(pid).strip() == "":
            continue
        items.append(MaterialRequisitionItemCreate(
            product_id=int(pid),
            product_name=pname,
            unit=u,
            requested_quantity=req_qty,
            issued_quantity=iss_qty,
            price=pr,
            amount=amt,
        ))

    obj_in = MaterialRequisitionUpdate(
        organization_id=organization_id,
        warehouse_id=warehouse_id,
        department_id=department_id,
        employee_id=employee_id,
        requisition_number=requisition_number,
        requisition_date=requisition_date,
        production_order_id=production_order_id if production_order_id else None,
        purpose=purpose if purpose else None,
        status=status,
        issued_by_id=issued_by_id if issued_by_id else None,
        received_by_id=received_by_id if received_by_id else None,
        items=items,
    )
    db_obj = crud_requisition.get_material_requisition(db, requisition_id)
    crud_requisition.update_material_requisition(db, db_obj, obj_in)
    return RedirectResponse(url="/requisitions", status_code=303)

@router.get("/{requisition_id}/print", response_class=HTMLResponse)
def requisition_print(requisition_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_requisition.get_material_requisition(db, requisition_id)
    return templates.TemplateResponse("requisitions/print.html", {"request": request, "requisition": item})

@router.get("/{requisition_id}/delete", response_class=HTMLResponse)
def delete_requisition_form(requisition_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_requisition.get_material_requisition(db, requisition_id)
    return templates.TemplateResponse("requisitions/delete.html", {"request": request, "requisition": item})

@router.post("/{requisition_id}/delete")
def delete_requisition(requisition_id: int, db: Session = Depends(get_db)):
    db_obj = crud_requisition.get_material_requisition(db, requisition_id)
    crud_requisition.delete_material_requisition(db, db_obj)
    return RedirectResponse(url="/requisitions", status_code=303)

@router.get("/{requisition_id}/approve", response_class=RedirectResponse)
def approve_requisition(requisition_id: int, db: Session = Depends(get_db)):
    db_obj = crud_requisition.get_material_requisition(db, requisition_id)
    if db_obj:
        db_obj.status = "утвержден"
        db.commit()
    return RedirectResponse(url=f"/requisitions/{requisition_id}", status_code=303)

@router.get("/{requisition_id}/complete", response_class=RedirectResponse)
def complete_requisition(requisition_id: int, db: Session = Depends(get_db)):
    db_obj = crud_requisition.get_material_requisition(db, requisition_id)
    if db_obj:
        db_obj.status = "выполнен"
        db.commit()
    return RedirectResponse(url=f"/requisitions/{requisition_id}", status_code=303)