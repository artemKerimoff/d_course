from app.database import SessionLocal
from app.crud import invoice as crud_invoice

db = SessionLocal()
try:
    items = crud_invoice.get_invoices(db)
    print('ok, got', len(items), 'invoices')
    for i in items[:5]:
        print(i)
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
