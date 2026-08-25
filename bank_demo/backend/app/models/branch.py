from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .atm import ATM
    from .technician import Technician

class Branch(Base):
    __tablename__ = 'branches'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    location_region: Mapped[str] = mapped_column(String(50))
    capacity: Mapped[int] = mapped_column(Integer)
    supervisor_id: Mapped[int] = mapped_column(Integer)

    atms: Mapped[list["ATM"]] = relationship(back_populates="branch")
    technicians: Mapped[list["Technician"]] = relationship(back_populates="branches")

    def __repr__(self) -> str:
            return (f"ID {self.id}, name: {self.name}, location: {self.location_region}, capacity: {self.capacity}")
    


"""from typing import ClassVar

class Branch:

    registry: ClassVar[list["Branch"]] = []

    def __init__(self, branch_id: int, name: str, location_region: str, capacity: int, manager_id: int):
        self.id = branch_id
        self.name = name
        self.location_region = location_region
        self.capacity = capacity
        self.manager_id = manager_id 
        Branch.registry.append(self)

    def __repr__(self) -> str:
        return (f"ID {self.id}, name: {self.name}, location: {self.location_region}, capacity: {self.capacity}, manager id: {self.manager_id}")

    @classmethod
    def find_by_id(cls, branch_id: int) -> "Branch | None":
        for branch in cls.registry:
            if branch.id == branch_id:
                return branch

        return None"""