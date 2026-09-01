from pydantic import BaseModel, ConfigDict, Field

from app.models import Technician_RBAC

class UserBase(BaseModel):
    username: str = Field(min_length=5, max_length=50)
    role: Technician_RBAC

class UserCreate(UserBase):
    """when a user is created, that is when you want to set the password"""
    password: str

class UserRead(UserBase):
    """Shape of an atm in any API Response"""
    id: int
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
