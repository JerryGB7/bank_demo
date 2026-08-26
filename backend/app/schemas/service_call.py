
from pydantic import BaseModel, ConfigDict
from app.models.service_call import Service_Call_Priority, Service_Call_Status


class ServiceCallBase(BaseModel):
    title: str
    priority: Service_Call_Priority = Service_Call_Priority.LOW
    status: Service_Call_Status = Service_Call_Status.PENDING
    atm_id: int
    technician_id: int
    

    model_config = ConfigDict(from_attributes=True)

class ServiceCallCreate(ServiceCallBase):
    """Shape of the request body for POST /atms"""


class ServiceCallRead(ServiceCallBase):
    """Shape of an atm in any API Response"""
    id: int
    model_config = ConfigDict(from_attributes=True)