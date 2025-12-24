from app.core.config import DATABASE_URL
from sqlalchemy import create_engine, text

engine = create_engine(DATABASE_URL)
sql = text(
    "ALTER TABLE material_requisitions ALTER COLUMN warehouse_id TYPE varchar(255) USING warehouse_id::varchar;"
)
with engine.connect() as conn:
    conn.execute(sql)
    conn.commit()
print('ALTER TABLE applied')
