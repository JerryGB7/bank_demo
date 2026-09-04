# Import the validation utilities and the ATM status enum used by the schema.
from pydantic import BaseModel, Field, ConfigDict
from app.models.atm import ATMStatus


# Shared ATM fields used across all ATM-related request/response schemas.
# This keeps validation consistent and ensures every ATM record includes the
# required business data needed by the API and database layer.
class ATMBase(BaseModel):
    serial_number: int
    model: str = Field(min_length=1, max_length=50)
    status: ATMStatus = ATMStatus.OPERATIONAL
    cash_level: int = Field(ge=0, le=100)
    branch_id: int
    technician_id: int | None = None


# Request payload for creating a new ATM.
# It reuses ATMBase so the same validation rules apply to incoming create
# requests, making the API contract clear and preventing invalid data.
class ATMCreate(ATMBase):
    """Shape of the request body for POST /atms"""


# Response model for reading ATM data back to the client.
# Including the generated database id and allowing ORM object conversion helps
# the API serialize ATM records directly from SQLAlchemy models.
class ATMRead(ATMBase):
    """Shape of an atm in any API Response"""
    id: int
    model_config = ConfigDict(from_attributes=True)


# Response model for discrepancy data linking an ATM and technician context.
# This schema makes it easy to return related values from joined records in a
# structured way while keeping the field names explicit for API consumers.
class DiscrepancyRead(BaseModel):
    ATM_id: int
    ATM_branch_id: int
    ATM_technician_id: int
    technician_id: int
    technician_branch_id: int
    model_config = ConfigDict(from_attributes=True)