"""Seed script for Pegasus Ops."""
from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.tool import Tool
from app.models.user import User
from app.core.security import hash_password
from app.services.tool_catalog import TOOLS


def run() -> None:
    db = SessionLocal()
    try:
        if not db.scalar(select(User).where(User.email == "admin@pegasus.local")):
            db.add(User(name="Pegasus Admin", email="admin@pegasus.local", password_hash=hash_password("Admin12345!"), role="admin"))
        for slug, name, category in TOOLS:
            if not db.scalar(select(Tool).where(Tool.slug == slug)):
                db.add(Tool(slug=slug, name=name, category=category, description=f"{name} utility for operations workflow."))
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    run()
