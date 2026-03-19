from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.activity import FavoriteTool, UsageHistory
from app.models.tool import Tool
from app.models.user import User
from app.services.tool_catalog import catalog_summary, featured_tools, filter_tools, list_categories, new_tools, sort_tools

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def landing(request: Request):
    summary = catalog_summary()
    return templates.TemplateResponse(
        "landing/index.html",
        {"request": request, "title": "Pegasus Ops", "summary": summary, "featured": featured_tools(limit=4), "new_tools": new_tools(limit=10)},
    )


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request, "title": "Login | Pegasus Ops"})


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    query: str | None = None,
    category: str | None = None,
    sort_by: str = "name",
):
    db_tools = db.scalars(select(Tool).limit(50)).all()
    favorites = db.scalars(select(FavoriteTool).where(FavoriteTool.user_id == user.id)).all()
    history = db.scalars(select(UsageHistory).where(UsageHistory.user_id == user.id).limit(10)).all()

    catalog_tools = sort_tools(filter_tools(category=category, query=query), sort_by=sort_by)
    selected_categories = list_categories()
    summary = catalog_summary()

    return templates.TemplateResponse(
        "dashboard/index.html",
        {
            "request": request,
            "title": "Dashboard | Pegasus Ops",
            "user": user,
            "tools": db_tools,
            "favorites": favorites,
            "history": history,
            "catalog_tools": catalog_tools[:12],
            "featured": featured_tools(limit=6),
            "new_tools": new_tools(limit=10),
            "summary": summary,
            "query": query or "",
            "category": category or "",
            "sort_by": sort_by,
            "categories": selected_categories,
        },
    )


@router.get("/settings", response_class=HTMLResponse)
def settings(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse("dashboard/settings.html", {"request": request, "title": "Settings | Pegasus Ops", "user": user})
