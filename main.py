from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from database import SessionLocal
from models import Expense
from routes import expenses
import os
import  models


app = FastAPI(title="Finance Tracker")
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/dashboard")


@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    expenses = db.query(Expense).all()
    print(f"📦 Найдено {len(expenses)} расходов в базе")
    db.close()


# Подключаем маршруты
app.include_router(expenses.router)

# Подключаем шаблоны
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))


# Функция для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    db = SessionLocal()
    expenses = db.query(models.Expense).all()

    # группировка
    category_totals = {}
    for e in expenses:
        category_totals[e.category] = category_totals.get(e.category, 0) + e.amount

    categories = list(category_totals.keys())
    totals = list(category_totals.values())

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "expenses": expenses,
        "categories": categories,
        "totals": totals
    })
