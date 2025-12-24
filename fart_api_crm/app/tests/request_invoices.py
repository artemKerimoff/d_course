import traceback
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
try:
    resp = client.get('/invoices')
    print('STATUS', resp.status_code)
    print(resp.text)
except Exception:
    traceback.print_exc()
