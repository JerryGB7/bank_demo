from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
      from .branch import Branch
      from .service_call import ServiceCall
      from .atm import ATM

class Technician(Base):
    __tablename__ = "technicians"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    branch_id: Mapped[int] = mapped_column(Integer, ForeignKey("branches.id"))

     # Each technician belongs to one branch.
    branches: Mapped["Branch"] = relationship(back_populates="technicians")
    atms: Mapped[list["ATM"]] = relationship(back_populates="technician")  
    service_calls: Mapped[list["ServiceCall"]] = relationship(back_populates="technicians")


    def __repr__(self) -> str:
            return (f"Technician attributes: {self.id}{self.name}")
