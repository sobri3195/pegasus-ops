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

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def landing(request: Request):
    return templates.TemplateResponse("landing/index.html", {"request": request, "title": "Pegasus Ops"})


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request, "title": "Login | Pegasus Ops"})


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tools = db.scalars(select(Tool).limit(50)).all()
    favorites = db.scalars(select(FavoriteTool).where(FavoriteTool.user_id == user.id)).all()
    history = db.scalars(select(UsageHistory).where(UsageHistory.user_id == user.id).limit(10)).all()
    return templates.TemplateResponse(
        "dashboard/index.html",
        {"request": request, "title": "Dashboard | Pegasus Ops", "user": user, "tools": tools, "favorites": favorites, "history": history},
    )


@router.get("/settings", response_class=HTMLResponse)
def settings(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse("dashboard/settings.html", {"request": request, "title": "Settings | Pegasus Ops", "user": user})
