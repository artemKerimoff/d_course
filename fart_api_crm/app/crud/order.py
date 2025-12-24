from __future__ import annotations
from sqlalchemy.orm import Session
from .. import models
from ..schemas import orders as schemas

def get_order(db: Session, id: int):
    return db.query(models.Order).filter(models.Order.id == id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).order_by(models.Order.order_date.desc()).offset(skip).limit(limit).all()

def create_order(db: Session, obj_in: schemas.OrderCreate):
    order = models.Order(
        organization_id=obj_in.organization_id,
        department_id=obj_in.department_id,
        employee_id=obj_in.employee_id,
        order_date=obj_in.order_date,
        order_number=obj_in.order_number,
        purpose=obj_in.purpose,
    )
    db.add(order)
    db.flush()

    # Добавляем позиции с ценами из продуктов
    for item in obj_in.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        db.add(models.OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            amount=item.amount,
            price=product.price if product else None
        ))

    db.commit()
    db.refresh(order)
    return order

def update_order(db: Session, db_obj: models.Order, obj_in: schemas.OrderUpdate):
    db_obj.organization_id = obj_in.organization_id
    db_obj.department_id = obj_in.department_id
    db_obj.employee_id = obj_in.employee_id
    db_obj.order_date = obj_in.order_date
    db_obj.order_number = obj_in.order_number
    db_obj.purpose = obj_in.purpose

    # Обновляем позиции
    db.query(models.OrderItem).filter(models.OrderItem.order_id == db_obj.id).delete()
    db.flush()

    for item in obj_in.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        db.add(models.OrderItem(
            order_id=db_obj.id,
            product_id=item.product_id,
            amount=item.amount,
            price=product.price if product else None
        ))

    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_order(db: Session, db_obj: models.Order):
    db.delete(db_obj)
    db.commit()