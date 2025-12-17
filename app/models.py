from app import db
from uuid import uuid4
from datetime import datetime
from sqlalchemy import func, DateTime
from sqlalchemy.orm import Mapped, mapped_column


def get_uuid() -> str:
    return str(uuid4())


class User(db.Base):
    __tablename__ = 'users'
    
    id: Mapped[str] = mapped_column(primary_key=True, default=get_uuid)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=func.now())
