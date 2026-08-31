# Imports from outside packages that aren't in our app.
# This allows us to use SQLAlchemy types and ORM features for our model.
from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, CheckConstraint, ForeignKey
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Imports from packages created in our app.
# Base provides the SQLAlchemy declarative base, and ATMStatus defines the ATM statuses.
from .base import Base
from .enums import ATMStatus

# Only import these classes when type checking is running.
# This avoids circular imports while still making type hints available.
if TYPE_CHECKING:
    from .branch import Branch
    from .technician import Technician
    from .service_call import ServiceCall


# ATM model representing an ATM machine in the database.
class ATM(Base):
    __tablename__ = "atms"

    # Database-level constraints for the table.
    # This ensures cash_level is always between 0 and 100.
    __table_args__ = (
        CheckConstraint("cash_level BETWEEN 0 AND 100", name="cash_level_range"),
    )

    # Primary key for the ATM record.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Basic ATM details.
    serial_number: Mapped[int] = mapped_column(Integer)
    model: Mapped[str] = mapped_column(String(50))

    # ATM status stored as a database enum with values from the ATMStatus enum.
    status: Mapped[ATMStatus] = mapped_column(
        SqlEnum(
            ATMStatus,
            name="atm_status",
            # Store the enum values in the database rather than the Python enum names,
            # keeping the DB representation compatible with the enum values.
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=ATMStatus.OPERATIONAL,
    )

    # Cash level and the IDs for the related branch and technician.
    cash_level: Mapped[int] = mapped_column(Integer)
    branch_id: Mapped[int] = mapped_column(Integer, ForeignKey("branches.id"))
    technician_id: Mapped[int] = mapped_column(Integer, ForeignKey("technicians.id"))

    # Relationships to related models.
    # An ATM belongs to one branch and one technician, and may have service calls.
    branch: Mapped["Branch"] = relationship(back_populates="atms")
    technician: Mapped["Technician"] = relationship(back_populates="atms")
    service_call: Mapped["ServiceCall"] = relationship(back_populates="atms")

    # Method to check whether the ATM is currently in maintenance.
    def needs_maintenance(self) -> bool:
        return self.status == ATMStatus.MAINTENANCE

    # String representation for debugging and logging.
    def __repr__(self) -> str:
        return (
            f"ATM (serial number = {self.serial_number}, cash_level: {self.cash_level}, "
            f"branch_id: {self.branch_id}, status: {self.status.value}"
        )
    
    
