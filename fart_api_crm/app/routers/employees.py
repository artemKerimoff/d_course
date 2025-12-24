from __future__ import annotations
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import employees as schemas
from ..crud import employee as crud
from ..templating import get_templates


templates = get_templates()
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def list_employees(request: Request, db: Session = Depends(get_db)):
    items = crud.get_employees(db)
    return templates.TemplateResponse("employees/list.html", {"request": request, "employees": items})

@router.get("/create", response_class=HTMLResponse)
def create_employee_form(request: Request):
    return templates.TemplateResponse("employees/create.html", {"request": request})

@router.post("/create")
def create_employee(
    last_name: str = Form(...),
    first_name: str = Form(...),
    middle_name: str | None = Form(None),
    post: str = Form(...),
    passport_series: str = Form(...),
    passport_number: str = Form(...),
    passport_issued_by: str = Form(...),
    passport_date_of_issue: str = Form(...),  # "YYYY-MM-DD"
    db: Session = Depends(get_db),
):
    obj_in = schemas.EmployeeCreate(
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name or None,
        post=post,
        passport_series=passport_series,
        passport_number=passport_number,
        passport_issued_by=passport_issued_by,
        passport_date_of_issue=passport_date_of_issue,  # pydantic конвертирует в date
    )
    crud.create_employee(db, obj_in)
    return RedirectResponse(url="/employees", status_code=303)

@router.get("/{item_id}/edit", response_class=HTMLResponse)
def edit_employee_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud.get_employee(db, item_id)
    return templates.TemplateResponse("employees/edit.html", {"request": request, "item": item})

@router.post("/{item_id}/edit")
def update_employee(
    item_id: int,
    last_name: str = Form(...),
    first_name: str = Form(...),
    middle_name: str | None = Form(None),
    post: str = Form(...),
    passport_series: str = Form(...),
    passport_number: str = Form(...),
    passport_issued_by: str = Form(...),
    passport_date_of_issue: str = Form(...),
    db: Session = Depends(get_db),
):
    db_obj = crud.get_employee(db, item_id)
    obj_in = schemas.EmployeeUpdate(
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name or None,
        post=post,
        passport_series=passport_series,
        passport_number=passport_number,
        passport_issued_by=passport_issued_by,
        passport_date_of_issue=passport_date_of_issue,
    )
    crud.update_employee(db, db_obj, obj_in)
    return RedirectResponse(url="/employees", status_code=303)

@router.get("/{item_id}/delete", response_class=HTMLResponse)
def delete_employee_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud.get_employee(db, item_id)
    return templates.TemplateResponse("employees/delete.html", {"request": request, "item": item})

@router.post("/{item_id}/delete")
def delete_employee(item_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_employee(db, item_id)
    crud.delete_employee(db, db_obj)
    return RedirectResponse(url="/employees", status_code=303)