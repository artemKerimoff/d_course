from __future__ import annotations
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .database import init_db
from .templating import get_templates
from .routers import accounts
from .routers import organizations
from .routers import employees
from .routers import units
from .routers import products
from .routers import customers
from .routers import departments
from .routers import positions
from .routers import proxies
from .routers import orders
from .routers import invoices
from .routers import material_requisitions


app = FastAPI(title="FastAPI", debug=True)

# Используем общий экземпляр шаблонов
templates = get_templates()

# Подключаем статику
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
async def on_startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(units.router, prefix="/units", tags=["units"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(departments.router, prefix="/departments", tags=["departments"])
app.include_router(positions.router, prefix="/positions", tags=["positions"])
app.include_router(proxies.router, prefix="/proxies", tags=["proxies"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(invoices.router, prefix="/invoices", tags=["invoices"])
app.include_router(material_requisitions.router, prefix="/requisitions", tags=["requisitions"])