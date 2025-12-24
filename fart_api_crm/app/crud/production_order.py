from typing import List
from sqlalchemy.orm import Session


def get_production_orders(db: Session) -> List:
    """Stub: return list of production orders. Replace with real DB query when model exists."""
    try:
        # If a ProductionOrder model exists, attempt to query it
        from ..models import production_orders  # type: ignore
        return db.query(production_orders.ProductionOrder).all()
    except Exception:
        return []
