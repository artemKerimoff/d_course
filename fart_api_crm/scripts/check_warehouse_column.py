from sqlalchemy import create_engine, text
from app.core.config import DATABASE_URL

e = create_engine(DATABASE_URL)
with e.connect() as conn:
    res = conn.execute(text("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'material_requisitions' AND column_name = 'warehouse_id'
    """))
    for row in res:
        print(row)
