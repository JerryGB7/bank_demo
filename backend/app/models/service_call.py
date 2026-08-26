from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import Service_Call_Priority, Service_Call_Status

if TYPE_CHECKING:
    from .technician import Technician
    from .atm import ATM

class ServiceCall(Base):
    __tablename__ = "service_calls"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    priority: Mapped[Service_Call_Priority] = mapped_column(
                    SqlEnum(Service_Call_Priority, name="service_call_priority", values_callable=lambda enum_cls:[member.value for member in enum_cls]),
                    default=Service_Call_Priority.LOW)
    status: Mapped[Service_Call_Status] = mapped_column(
            SqlEnum(Service_Call_Status, name="service_call_status", values_callable=lambda enum_cls:[member.value for member in enum_cls]),
            default=Service_Call_Status.PENDING)
    atm_id: Mapped[int] = mapped_column(Integer, ForeignKey("atms.id"))
    technician_id: Mapped[int] = mapped_column(Integer, ForeignKey("technicians.id"))
    

    atms: Mapped["ATM"] = relationship(back_populates="service_call")    
    technicians: Mapped["Technician"] = relationship(back_populates="service_calls")

    def __repr__(self) -> str:
        return (f"Service call attributes: {self.title}{self.atm_id}{self.technician_id}{self.priority}{self.status}")

"""from typing import ClassVar
from .enums import Service_Call_Priority, Service_Call_Status

class ServiceCall:

    registry: ClassVar[list["ServiceCall"]] = []

    def __init__(self, service_call_id: int, title: str, atm_id: int, technician_id: int, priority: Service_Call_Priority = Service_Call_Priority.LOW, status: Service_Call_Status = Service_Call_Status.PENDING):
        self.id = service_call_id
        self.title = title
        self.atm_id = atm_id
        self.technician_id = technician_id
        self.priority = priority
        self.status = status
        ServiceCall.registry.append(self)

    def mark_completed(self) -> None:
        self.status = Service_Call_Status.COMPLETED

    def mark_failed(self) -> None:
        self.status = Service_Call_Status.FAILED

    def set_critical(self) -> None:
        self.priority = Service_Call_Priority.CRITICAL

    def set_medium(self) -> None:
        self.priority = Service_Call_Priority.MEDIUM

    @classmethod
    def find_by_id(cls, service_call_id: int) -> "ServiceCall | None":
        for service_call in cls.registry:
            if service_call_id == service_call.id:
                return service_call

        return None

    def __repr__(self) -> str:
        return (f"Service call attributes: {self.title}{self.atm_id}{self.technician_id}{self.priority}{self.status}")"""
        