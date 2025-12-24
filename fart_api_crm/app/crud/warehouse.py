from typing import List
from sqlalchemy.orm import Session


def get_warehouses(db: Session) -> List:
    """Stub: return list of warehouses. Replace with real DB query when model exists."""
    try:
        # If a Warehouse model exists, attempt to query it
        from ..models import warehouses  # type: ignore
        return db.query(warehouses.Warehouse).all()
    except Exception:
        return []
