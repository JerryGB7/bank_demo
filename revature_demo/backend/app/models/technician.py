from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .enums import Technician_RBAC
from .base import Base

if TYPE_CHECKING:
      from .service_call import ServiceCall

class Technician(Base):
    __tablename__ = "technicians"

    id: Mapped[int] = mapped_column(primary_key=True)
    rbac: Mapped[Technician_RBAC] = mapped_column(
            SqlEnum(Technician_RBAC, name="technician_rbac", values_callable=lambda enum_cls:[member.value for member in enum_cls]))

    service_calls: Mapped["ServiceCall"] = relationship(back_populates="technicians")

    def __repr__(self) -> str:
            return (f"Technician attributes: {self.id}{self.RBAC}")

"""from typing import ClassVar
from .enums import Technician_RBAC

class Technician:
    registry: ClassVar[list["Technician"]] = []

    def __init__(self, technician_id: int, RBAC: Technician_RBAC):
        self.id = technician_id
        self.RBAC = RBAC
        Technician.registry.append(self)

    @classmethod
    def find_by_id(cls, technician_id: int) -> "Technician | None":
        for technician in cls.registry:
            if technician_id == technician_id:
                return technician

        return None

    def find_manager(self) -> Technician:
        return self.RBAC == Technician_RBAC.OPERATION_MANAGER

    def __repr__(self) -> str:
        return (f"Technician attributes: {self.id}{self.RBAC}")"""