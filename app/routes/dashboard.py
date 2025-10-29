from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import date
from typing import List
from app.core.auth import get_current_user, get_db
from app.models.transaction import Transaction
from app.models.category import Category
from app.models.user import User
from fastapi.responses import HTMLResponse

router = APIRouter()

# Resumo mensal
@router.get("/summary")
def get_summary(
    month: int,
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Total de receitas
    income = db.query(func.coalesce(func.sum(Transaction.amount), 0))\
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.type == "income",
            extract("month", Transaction.date) == month,
            extract("year", Transaction.date) == year
        ).scalar()

    # Total de despesas
    expense = db.query(func.coalesce(func.sum(Transaction.amount), 0))\
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.type == "expense",
            extract("month", Transaction.date) == month,
            extract("year", Transaction.date) == year
        ).scalar()

    # Top categorias de despesa
    top_categories = db.query(
            Category.name,
            func.sum(Transaction.amount).label("total")
        )\
        .join(Category, Category.id == Transaction.category_id)\
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.type == "expense",
            extract("month", Transaction.date) == month,
            extract("year", Transaction.date) == year
        )\
        .group_by(Category.name)\
        .order_by(func.sum(Transaction.amount).desc())\
        .limit(5)\
        .all()

    return {
        "income": float(income),
        "expense": float(expense),
        "balance": float(income - expense),
        "top_categories": [{"category": c[0], "total": float(c[1])} for c in top_categories]
    }

# Tendências (últimos N meses)
@router.get("/trends")
def get_trends(
    months: int = 6,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    start_year = today.year if today.month - months + 1 > 0 else today.year - 1
    start_month = (today.month - months + 1) % 12 or 12

    results = db.query(
            extract("year", Transaction.date).label("year"),
            extract("month", Transaction.date).label("month"),
            Transaction.type,
            func.sum(Transaction.amount).label("total")
        )\
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.date >= date(start_year, start_month, 1)
        )\
        .group_by("year", "month", Transaction.type)\
        .order_by("year", "month")\
        .all()

    # Organizar resultados em formato esperado
    trends = {}
    for year, month, t_type, total in results:
        key = f"{int(year)}-{int(month):02d}"
        if key not in trends:
            trends[key] = {"month": key, "income": 0.0, "expense": 0.0}
        trends[key][t_type] = float(total)

    return list(trends.values())

# retornação em HTML para integração com front-end

@router.get("/summary_html", response_class=HTMLResponse)
def get_summary_html(month: int, year: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = get_summary(month, year, db, current_user)
    html = f"""
    <p><strong>Receitas:</strong> R$ {data['income']:.2f}</p>
    <p><strong>Despesas:</strong> R$ {data['expense']:.2f}</p>
    <p><strong>Saldo:</strong> <span class="{'positive' if data['balance'] >= 0 else 'negative'}">R$ {data['balance']:.2f}</span></p>
    <h3>Top Categorias</h3>
    <ul>
        {''.join(f"<li>{c['category']} — R$ {c['total']:.2f}</li>" for c in data['top_categories'])}
    </ul>
    """
    return HTMLResponse(content=html)

@router.get("/trends_html", response_class=HTMLResponse)
def get_trends_html(months: int = 6, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = get_trends(months, db, current_user)
    rows = "".join(
        f"<tr><td>{item['month']}</td><td>R$ {item['income']:.2f}</td><td>R$ {item['expense']:.2f}</td></tr>"
        for item in data
    )
    html = f"""
    <table>
        <thead>
            <tr><th>Mês</th><th>Receitas</th><th>Despesas</th></tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    """
    return HTMLResponse(content=html)
