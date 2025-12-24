from __future__ import annotations
from sqlalchemy.orm import Session
from .. import models
from ..schemas import material_requisition as schemas

def get_material_requisition(db: Session, id: int):
    return db.query(models.MaterialRequisition).filter(models.MaterialRequisition.id == id).first()

def get_material_requisitions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MaterialRequisition).order_by(models.MaterialRequisition.requisition_date.desc()).offset(skip).limit(limit).all()

def create_material_requisition(db: Session, obj_in: schemas.MaterialRequisitionCreate):
    requisition = models.MaterialRequisition(
        organization_id=obj_in.organization_id,
        warehouse_id=obj_in.warehouse_id,
        department_id=obj_in.department_id,
        employee_id=obj_in.employee_id,
        requisition_number=obj_in.requisition_number,
        requisition_date=obj_in.requisition_date,
        production_order_id=obj_in.production_order_id,
        purpose=obj_in.purpose,
        status=obj_in.status,
        issued_by_id=obj_in.issued_by_id,
        received_by_id=obj_in.received_by_id,
    )
    db.add(requisition)
    db.flush()
    
    for item in obj_in.items:
        db.add(models.MaterialRequisitionItem(
            requisition_id=requisition.id,
            product_id=item.product_id,
            product_name=item.product_name,
            unit=item.unit,
            requested_quantity=item.requested_quantity,
            issued_quantity=item.issued_quantity,
            price=item.price,
            amount=item.amount,
        ))
    
    db.commit()
    db.refresh(requisition)
    return requisition

def update_material_requisition(db: Session, db_obj: models.MaterialRequisition, obj_in: schemas.MaterialRequisitionUpdate):
    # Обновляем основную информацию
    for field, value in obj_in.dict(exclude={'items'}).items():
        setattr(db_obj, field, value)
    
    # Обновляем позиции
    db.query(models.MaterialRequisitionItem).filter(
        models.MaterialRequisitionItem.requisition_id == db_obj.id
    ).delete()
    db.flush()
    
    for item in obj_in.items:
        db.add(models.MaterialRequisitionItem(
            requisition_id=db_obj.id,
            product_id=item.product_id,
            product_name=item.product_name,
            unit=item.unit,
            requested_quantity=item.requested_quantity,
            issued_quantity=item.issued_quantity,
            price=item.price,
            amount=item.amount,
        ))
    
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_material_requisition(db: Session, db_obj: models.MaterialRequisition):
    db.delete(db_obj)
    db.commit()