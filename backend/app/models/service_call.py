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


        