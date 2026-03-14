from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas.auth import RegisterInput
from app.services.auth_service import authenticate_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = register_user(db, RegisterInput(name=name, email=email, password=password))
    response = RedirectResponse(url="/dashboard", status_code=303)
    token = create_access_token(str(user.id), {"role": user.role})
    response.set_cookie("access_token", token, httponly=True)
    return response


@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(db, email, password)
    if not user:
        return RedirectResponse(url="/login?error=1", status_code=303)
    response = RedirectResponse(url="/dashboard", status_code=303)
    token = create_access_token(str(user.id), {"role": user.role})
    response.set_cookie("access_token", token, httponly=True)
    return response


@router.get("/logout")
def logout(request: Request):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response
