from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, CheckConstraint, ForeignKey, Numeric
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import ATMStatus

if TYPE_CHECKING:
    from .branch import Branch
    from .technician import Technician
    from .service_call import ServiceCall


class ATM(Base):
    __tablename__ = "atms"

    __table_args__ = (
        CheckConstraint("cash_level BETWEEN 0 AND 100", name="cash_level_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    serial_number: Mapped[int] = mapped_column(Integer)
    model: Mapped[str] = mapped_column(String(50))
    status: Mapped[ATMStatus] = mapped_column(
        SqlEnum(ATMStatus, name="atm_status", values_callable=lambda enum_cls:[member.value for member in enum_cls]),
        default=ATMStatus.OPERATIONAL)
    cash_level: Mapped[int] = mapped_column(Integer)
    branch_id: Mapped[int] = mapped_column(Integer, ForeignKey("branches.id"))
    technician_id: Mapped[int] = mapped_column(Integer, ForeignKey("technicians.id"))

    branch: Mapped["Branch"] = relationship(back_populates="atms")
    technician: Mapped["Technician"] = relationship(back_populates="atms")
    service_call: Mapped["ServiceCall"] = relationship(back_populates="atms")


    def needs_maintenance(self) -> bool:
        return self.status == ATMStatus.MAINTENANCE

    def __repr__(self) -> str:
        return (f"ATM (serial number = {self.serial_number}, cash_level: {self.cash_level}, branch_id: {self.branch_id}, status: {self.status.value}")
    
    

"""from typing import ClassVar

from .enums import ATMStatus

class ATM:
    registry: ClassVar[list["ATM"]] = []

    low_cash_threshold: ClassVar[int] = 20

    def __init__(self, atm_id: int, serial_number: str, model: str, cash_level: int, branch_id: int, status: ATMStatus = ATMStatus.OPERATIONAL):
        self.id = atm_id
        self.serial_number = serial_number
        self.model = model
        self.status = status 
        self.cash_level = self.validate_cash_level(cash_level)
        self.branch_id = branch_id
        ATM.registry.append(self)


    @staticmethod
    def validate_cash_level(level: int) -> int:
        if level < 0:
            print(f"Warning: cash level {level} below 0, clamping to 0")
            return 0
        if level > 100:
            print(f"Warning: cash level {level} above 100, clamping to 100")
            return 100
        return level

    def is_low_cash(self, threshold: int | None = None) -> bool:
        limit = threshold if threshold is not None else ATM.low_cash_threshold
        return self.cash_level < limit

    def needs_maintenance(self) -> bool:
        return self.status == ATMStatus.MAINTENANCE

    @classmethod
    def find_by_id(cls, atm_id: int) -> "ATM | None":
        for atm in cls.registry:
            if atm.id == atm_id:
                return atm

        return None

    def __repr__(self) -> str:
        return (f"ATM (serial number = {self.serial_number}, cash_level: {self.cash_level}, branch_id: {self.branch_id}, status: {self.status.value}")
"""