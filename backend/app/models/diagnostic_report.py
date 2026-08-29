"""
Diagnostic Log Model - Day 3 SQLALchemy ORM version
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .service_call import ServiceCall

class DiagnosticReport(Base):
    __tablename__ = "diagnostic_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_call_id: Mapped[int] = mapped_column(Integer, ForeignKey("service_calls.id"))
    file_url: Mapped[str] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    #server_default=func.now() sets the default value of the created_at column
    #to the current timestamp when a new record is inserted into the database
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    service_call: Mapped["ServiceCall"] = relationship(back_populates="diagnostic_reports")

    def __repr__(self) -> str:
        return (f"DiagnosticReport(id={self.id}, service_call_id={self.service_call_id}, "
                f"file_url={self.file_url!r})")