from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas.auth import RegisterInput
from app.services.auth_service import EmailAlreadyRegisteredError, authenticate_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


def _set_session_cookie(response: RedirectResponse, token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24,
    )


@router.post("/register")
def register(name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    try:
        user = register_user(db, RegisterInput(name=name, email=email, password=password))
    except EmailAlreadyRegisteredError:
        return RedirectResponse(url="/login?error=email_used", status_code=303)

    response = RedirectResponse(url="/dashboard", status_code=303)
    token = create_access_token(str(user.id), {"role": user.role})
    _set_session_cookie(response, token)
    return response


@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(db, email, password)
    if not user:
        return RedirectResponse(url="/login?error=1", status_code=303)
    response = RedirectResponse(url="/dashboard", status_code=303)
    token = create_access_token(str(user.id), {"role": user.role})
    _set_session_cookie(response, token)
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response
