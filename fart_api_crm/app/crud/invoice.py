from __future__ import annotations
from sqlalchemy.orm import Session
from .. import models
from ..schemas import invoice as schemas

def get_invoice(db: Session, id: int):
    return db.query(models.Invoice).filter(models.Invoice.id == id).first()

def get_invoices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Invoice).order_by(models.Invoice.invoice_date.desc()).offset(skip).limit(limit).all()

def create_invoice(db: Session, obj_in: schemas.InvoiceCreate):
    invoice = models.Invoice(
        organization_id=obj_in.organization_id,
        supplier_id=obj_in.supplier_id,
        invoice_number=obj_in.invoice_number,
        invoice_date=obj_in.invoice_date,
        payment_due_date=obj_in.payment_due_date,
        total_without_vat=obj_in.total_without_vat,
        vat_amount=obj_in.vat_amount,
        total_with_vat=obj_in.total_with_vat,
        contract_number=obj_in.contract_number,
        contract_date=obj_in.contract_date,
        is_paid=obj_in.is_paid,
        is_received=obj_in.is_received,
    )
    db.add(invoice)
    db.flush()
    
    for item in obj_in.items:
        db.add(models.InvoiceItem(
            invoice_id=invoice.id,
            product_id=item.product_id,
            product_name=item.product_name,
            unit=item.unit,
            quantity=item.quantity,
            price=item.price,
            vat_rate=item.vat_rate,
            amount_without_vat=item.amount_without_vat,
            vat_amount=item.vat_amount,
            amount_with_vat=item.amount_with_vat,
        ))
    
    db.commit()
    db.refresh(invoice)
    return invoice

def update_invoice(db: Session, db_obj: models.Invoice, obj_in: schemas.InvoiceUpdate):
    # Обновляем основную информацию
    for field, value in obj_in.dict(exclude={'items'}).items():
        setattr(db_obj, field, value)
    
    # Обновляем позиции
    db.query(models.InvoiceItem).filter(models.InvoiceItem.invoice_id == db_obj.id).delete()
    db.flush()
    
    for item in obj_in.items:
        db.add(models.InvoiceItem(
            invoice_id=db_obj.id,
            product_id=item.product_id,
            product_name=item.product_name,
            unit=item.unit,
            quantity=item.quantity,
            price=item.price,
            vat_rate=item.vat_rate,
            amount_without_vat=item.amount_without_vat,
            vat_amount=item.vat_amount,
            amount_with_vat=item.amount_with_vat,
        ))
    
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_invoice(db: Session, db_obj: models.Invoice):
    db.delete(db_obj)
    db.commit()