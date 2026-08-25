from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.service_call import ServiceCallCreate,ServiceCallRead
from app.dependencies import get_db, get_current_user, require_role
from app.models import ServiceCall, User, Technician_RBAC
from app.models.enums import Service_Call_Priority, Service_Call_Status

router = APIRouter(prefix="/service_calls", tags=["service_calls"])

@router.get("", response_model = list[ServiceCallRead])
async def list_service_calls(db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)):
    # need a way to interact with the db
    # we are dependent on the session object 
    # create our statement for the db
    statement = select(ServiceCall)


    result = await db.execute(statement)
    return list(result.scalars().all())


# get a specific atm by its id
@router.get("/{service_call_id}", response_model=ServiceCallRead)
async def get_service_call(service_call_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)) -> ServiceCall:
    service_call = await db.get(ServiceCall, service_call_id)

    if service_call is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ATM with {service_call_id} not found"
        )
    return service_call

# Post requests are used for creating new resources or altering state
@router.post("", response_model=ServiceCallRead, status_code=status.HTTP_201_CREATED)
async def create_service_call(payload: ServiceCallCreate, db: AsyncSession = Depends(get_db), 
                     _: User=Depends(require_role(Technician_RBAC.OPERATION_MANAGER))):
   servicecall = ServiceCall(**payload.model_dump())

   db.add(servicecall)
   await db.commit()
   await db.refresh(servicecall)
   return servicecall

@router.patch("/{service_call_id}/status", response_model=ServiceCallRead, status_code=status.HTTP_202_ACCEPTED)
async def update_call_status(
    service_call_id: int,
    new_status: Service_Call_Status = Query(...),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(Technician_RBAC.FIELD_TECHNICIAN, Technician_RBAC.OPERATION_MANAGER)),
) -> ServiceCall:
    if new_status not in (Service_Call_Status.COMPLETED, Service_Call_Status.FAILED):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be complete or failed",
        )

    service_call = await db.get(ServiceCall, service_call_id)
    if service_call is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service call with {service_call_id} not found",
        )

    service_call.status = new_status
    await db.commit()
    await db.refresh(service_call)
    return service_call