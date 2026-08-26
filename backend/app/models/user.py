from __future__ import annotations

from sqlalchemy import Boolean, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .enums import Technician_RBAC

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[String] = mapped_column(String(50), unique=True,index=True)
    # in a real app, you never want to store a raw password in the database
    # instead we store a hashed version of the password
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[Technician_RBAC] = mapped_column(
        SQLEnum(
            Technician_RBAC,
            name = "technician-rbac",
            values_callable=lambda enum_cls: [member.value for member in enum_cls]
        )
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self):
        return (f"User: {self.username}, id{self.id}, role={self.role.value}")

