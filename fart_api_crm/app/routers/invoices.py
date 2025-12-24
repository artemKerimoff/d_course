from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..templating import get_templates
from ..crud import invoice as crud_invoice
from ..crud import organization as crud_org
from ..crud import product as crud_prod
from ..schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceItemCreate

templates = get_templates()
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def list_invoices(request: Request, db: Session = Depends(get_db)):
    items = crud_invoice.get_invoices(db)
    return templates.TemplateResponse("invoices/list.html", {"request": request, "invoices": items})

@router.get("/create", response_class=HTMLResponse)
def create_invoice_form(request: Request, db: Session = Depends(get_db)):
    orgs = crud_org.get_organizations(db)
    suppliers = crud_org.get_organizations(db)  # Поставщики - тоже организации
    prods = crud_prod.get_products(db)
    return templates.TemplateResponse(
        "invoices/create.html",
        {
            "request": request, 
            "orgs": orgs, 
            "suppliers": suppliers, 
            "prods": prods
        }
    )

@router.post("/create")
def create_invoice(
    organization_id: int = Form(...),
    supplier_id: int = Form(...),
    invoice_number: str = Form(...),
    invoice_date: str = Form(...),
    payment_due_date: str = Form(None),
    total_without_vat: float = Form(None),
    vat_amount: float = Form(None),
    total_with_vat: float = Form(None),
    contract_number: str = Form(""),
    contract_date: str = Form(None),
    is_paid: bool = Form(False),
    is_received: bool = Form(False),
    product_id: List[int] = Form([]),
    product_name: List[str] = Form([]),
    unit: List[str] = Form([]),
    quantity: List[float] = Form([]),
    price: List[float] = Form([]),
    vat_rate: List[float] = Form([]),
    amount_without_vat: List[float] = Form([]),
    item_vat_amount: List[float] = Form([]),
    amount_with_vat: List[float] = Form([]),
    db: Session = Depends(get_db),
):
    # Build items; compute amounts on server if not provided
    items = []
    total_no = 0.0
    total_vat = 0.0
    total_with = 0.0
    for pid, pname, u, qty, pr, vat, amt_no_vat, vat_amt, amt_with_vat in zip(
        product_id, product_name, unit, quantity, price, vat_rate,
        amount_without_vat, item_vat_amount, amount_with_vat
    ):
        if str(pid).strip() == "":
            continue
        q = float(qty or 0)
        p = float(pr or 0)
        vr = float(vat or 0)
        # ensure product_name and unit are filled (in case JS didn't set them)
        if (not pname or str(pname).strip() == '') and pid:
            prod = crud_prod.get_product(db, int(pid)) if pid else None
            if prod:
                pname = getattr(prod, 'name', pname)
                try:
                    u = prod.unit.name if prod.unit else u
                except Exception:
                    u = u
        # compute amounts if not provided
        no_vat = float(amt_no_vat) if (amt_no_vat is not None and str(amt_no_vat) != '') else round(q * p, 2)
        vat_amount_item = float(vat_amt) if (vat_amt is not None and str(vat_amt) != '') else round(no_vat * (vr / 100.0), 2)
        with_vat = float(amt_with_vat) if (amt_with_vat is not None and str(amt_with_vat) != '') else round(no_vat + vat_amount_item, 2)

        total_no += no_vat
        total_vat += vat_amount_item
        total_with += with_vat

        items.append(InvoiceItemCreate(
            product_id=int(pid),
            product_name=pname,
            unit=u,
            quantity=q,
            price=p,
            vat_rate=vr,
            amount_without_vat=no_vat,
            vat_amount=vat_amount_item,
            amount_with_vat=with_vat,
        ))

    # if totals not provided by form, use computed
    total_without_vat = float(total_without_vat) if (total_without_vat is not None and str(total_without_vat) != '') else round(total_no, 2)
    vat_amount = float(vat_amount) if (vat_amount is not None and str(vat_amount) != '') else round(total_vat, 2)
    total_with_vat = float(total_with_vat) if (total_with_vat is not None and str(total_with_vat) != '') else round(total_with, 2)

    obj_in = InvoiceCreate(
        organization_id=organization_id,
        supplier_id=supplier_id,
        invoice_number=invoice_number,
        invoice_date=invoice_date,
        payment_due_date=payment_due_date if payment_due_date else None,
        total_without_vat=total_without_vat,
        vat_amount=vat_amount,
        total_with_vat=total_with_vat,
        contract_number=contract_number if contract_number else None,
        contract_date=contract_date if contract_date else None,
        is_paid=is_paid,
        is_received=is_received,
        items=items,
    )
    crud_invoice.create_invoice(db, obj_in)
    return RedirectResponse(url="/invoices", status_code=303)

@router.get("/{invoice_id}", response_class=HTMLResponse)
def invoice_detail(invoice_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_invoice.get_invoice(db, invoice_id)
    return templates.TemplateResponse("invoices/view.html", {"request": request, "invoice": item})

@router.get("/{invoice_id}/edit", response_class=HTMLResponse)
def edit_invoice_form(invoice_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_invoice.get_invoice(db, invoice_id)
    orgs = crud_org.get_organizations(db)
    suppliers = crud_org.get_organizations(db)
    prods = crud_prod.get_products(db)
    return templates.TemplateResponse(
        "invoices/edit.html",
        {
            "request": request, 
            "invoice": item, 
            "orgs": orgs, 
            "suppliers": suppliers, 
            "prods": prods
        }
    )

@router.post("/{invoice_id}/edit")
def update_invoice(
    invoice_id: int,
    organization_id: int = Form(...),
    supplier_id: int = Form(...),
    invoice_number: str = Form(...),
    invoice_date: str = Form(...),
    payment_due_date: str = Form(None),
    total_without_vat: float = Form(None),
    vat_amount: float = Form(None),
    total_with_vat: float = Form(None),
    contract_number: str = Form(""),
    contract_date: str = Form(None),
    is_paid: bool = Form(False),
    is_received: bool = Form(False),
    product_id: List[int] = Form([]),
    product_name: List[str] = Form([]),
    unit: List[str] = Form([]),
    quantity: List[float] = Form([]),
    price: List[float] = Form([]),
    vat_rate: List[float] = Form([]),
    amount_without_vat: List[float] = Form([]),
    item_vat_amount: List[float] = Form([]),
    amount_with_vat: List[float] = Form([]),
    db: Session = Depends(get_db),
):
    # Build items; compute amounts on server if not provided
    items = []
    total_no = 0.0
    total_vat = 0.0
    total_with = 0.0
    for pid, pname, u, qty, pr, vat, amt_no_vat, vat_amt, amt_with_vat in zip(
        product_id, product_name, unit, quantity, price, vat_rate,
        amount_without_vat, item_vat_amount, amount_with_vat
    ):
        if str(pid).strip() == "":
            continue
        q = float(qty or 0)
        p = float(pr or 0)
        vr = float(vat or 0)
        # ensure product_name and unit are filled for edit as well
        if (not pname or str(pname).strip() == '') and pid:
            prod = crud_prod.get_product(db, int(pid)) if pid else None
            if prod:
                pname = getattr(prod, 'name', pname)
                try:
                    u = prod.unit.name if prod.unit else u
                except Exception:
                    u = u
        no_vat = float(amt_no_vat) if (amt_no_vat is not None and str(amt_no_vat) != '') else round(q * p, 2)
        vat_amount_item = float(vat_amt) if (vat_amt is not None and str(vat_amt) != '') else round(no_vat * (vr / 100.0), 2)
        with_vat = float(amt_with_vat) if (amt_with_vat is not None and str(amt_with_vat) != '') else round(no_vat + vat_amount_item, 2)

        total_no += no_vat
        total_vat += vat_amount_item
        total_with += with_vat

        items.append(InvoiceItemCreate(
            product_id=int(pid),
            product_name=pname,
            unit=u,
            quantity=q,
            price=p,
            vat_rate=vr,
            amount_without_vat=no_vat,
            vat_amount=vat_amount_item,
            amount_with_vat=with_vat,
        ))

    # if totals not provided by form, use computed
    total_without_vat = float(total_without_vat) if (total_without_vat is not None and str(total_without_vat) != '') else round(total_no, 2)
    vat_amount = float(vat_amount) if (vat_amount is not None and str(vat_amount) != '') else round(total_vat, 2)
    total_with_vat = float(total_with_vat) if (total_with_vat is not None and str(total_with_vat) != '') else round(total_with, 2)

    obj_in = InvoiceUpdate(
        organization_id=organization_id,
        supplier_id=supplier_id,
        invoice_number=invoice_number,
        invoice_date=invoice_date,
        payment_due_date=payment_due_date if payment_due_date else None,
        total_without_vat=total_without_vat,
        vat_amount=vat_amount,
        total_with_vat=total_with_vat,
        contract_number=contract_number if contract_number else None,
        contract_date=contract_date if contract_date else None,
        is_paid=is_paid,
        is_received=is_received,
        items=items,
    )
    db_obj = crud_invoice.get_invoice(db, invoice_id)
    crud_invoice.update_invoice(db, db_obj, obj_in)
    return RedirectResponse(url="/invoices", status_code=303)

@router.get("/{invoice_id}/print", response_class=HTMLResponse)
def invoice_print(invoice_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_invoice.get_invoice(db, invoice_id)
    return templates.TemplateResponse("invoices/print.html", {"request": request, "invoice": item})

@router.get("/{invoice_id}/delete", response_class=HTMLResponse)
def delete_invoice_form(invoice_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_invoice.get_invoice(db, invoice_id)
    return templates.TemplateResponse("invoices/delete.html", {"request": request, "invoice": item})

@router.post("/{invoice_id}/delete")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    db_obj = crud_invoice.get_invoice(db, invoice_id)
    crud_invoice.delete_invoice(db, db_obj)
    return RedirectResponse(url="/invoices", status_code=303)

@router.get("/{invoice_id}/mark-paid", response_class=RedirectResponse)
def mark_invoice_paid(invoice_id: int, db: Session = Depends(get_db)):
    db_obj = crud_invoice.get_invoice(db, invoice_id)
    if db_obj:
        db_obj.is_paid = True
        db.commit()
    return RedirectResponse(url=f"/invoices/{invoice_id}", status_code=303)

@router.get("/{invoice_id}/mark-received", response_class=RedirectResponse)
def mark_invoice_received(invoice_id: int, db: Session = Depends(get_db)):
    db_obj = crud_invoice.get_invoice(db, invoice_id)
    if db_obj:
        db_obj.is_received = True
        db.commit()
    return RedirectResponse(url=f"/invoices/{invoice_id}", status_code=303)