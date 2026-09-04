from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import case, func, select

from app.schemas.service_call import ReliabilityMetric, ServiceCallCreate,ServiceCallRead
from app.dependencies import get_db, get_current_user, require_role
from app.models import ATM, ServiceCall, User, Technician_RBAC
from app.models.enums import Service_Call_Priority, Service_Call_Status

router = APIRouter(prefix="/service_calls", tags=["service_calls"])

#---------------------------------------------------------------------------------
# THIS SECTION IS FOR GET FUNCTIONS

@router.get("", response_model = list[ServiceCallRead])
async def list_service_calls(db: AsyncSession = Depends(get_db)):
    # need a way to interact with the db
    # we are dependent on the session object 
    # create our statement for the db
    statement = select(ServiceCall)


    result = await db.execute(statement)
    return list(result.scalars().all())


# get a specific atm by its id
@router.get("/service_call_id", response_model=ServiceCallRead)
async def get_service_call(service_call_id: int, db: AsyncSession = Depends(get_db)) -> ServiceCall:
    service_call = await db.get(ServiceCall, service_call_id)

    if service_call is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ATM with {service_call_id} not found"
        )
    return service_call

@router.get("/complete_failed_ratio", response_model=str)
async def complete_failed_service(db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)):
    total_statement = select(func.count()).select_from(ServiceCall)
    failed_statement = select(func.count()).select_from(ServiceCall).where(
        ServiceCall.status == Service_Call_Status.FAILED
    )
    # TODO join the atm ids to identify which service calls are assigned to the atms

    total_count = await db.scalar(total_statement)
    failed_count = await db.scalar(failed_statement)

    return (f"{failed_count / total_count * 100 if total_count else 0.0}%")


@router.get("/reliability_metrics", response_model=list[ReliabilityMetric])
async def get_reliability_metrics(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[ReliabilityMetric]:
    """Return completed and failed service-call ratios for each ATM model."""
    completed_count = func.count(case((ServiceCall.status == Service_Call_Status.COMPLETED, 1)))
    failed_count = func.count(case((ServiceCall.status == Service_Call_Status.FAILED, 1)))

    statement = (
        select(
            ATM.model.label("model"),
            completed_count.label("completed_count"),
            failed_count.label("failed_count"),
        )
        .join(ServiceCall, ServiceCall.atm_id == ATM.id)
        .where(ServiceCall.status.in_((Service_Call_Status.COMPLETED, Service_Call_Status.FAILED)))
        .group_by(ATM.model)
        .order_by(ATM.model)
    )

    rows = (await db.execute(statement)).mappings().all()
    return [
        ReliabilityMetric(
            model=row["model"],
            completed_count=row["completed_count"],
            failed_count=row["failed_count"],
            total_resolved=row["completed_count"] + row["failed_count"],
            completion_ratio=(row["completed_count"] / (row["completed_count"] + row["failed_count"])) * 100,
            failure_ratio=(row["failed_count"] / (row["completed_count"] + row["failed_count"])) * 100,
        )
        for row in rows
    ]


#-----------------------------------------------------------------------------------
# THIS SECTION IS FOR POST FUNCTIONS

# Post requests are used for creating new resources or altering state
@router.post("", response_model=ServiceCallRead, status_code=status.HTTP_201_CREATED)
async def create_service_call(payload: ServiceCallCreate, db: AsyncSession = Depends(get_db), 
                     _: User=Depends(require_role(Technician_RBAC.OPERATION_MANAGER))):
   servicecall = ServiceCall(**payload.model_dump())

   db.add(servicecall)
   await db.commit()
   await db.refresh(servicecall)
   return servicecall

#-----------------------------------------------------------------------------------

# THIS SECTION IS FOR POST FUNCTIONS
@router.patch("/{service_call_id}/status", response_model=ServiceCallRead, status_code=status.HTTP_202_ACCEPTED)
async def update_call_status(
    service_call_id: int,
    new_status: Service_Call_Status = Query(...),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(Technician_RBAC.FIELD_TECHNICIAN, Technician_RBAC.OPERATION_MANAGER)),
) -> ServiceCall:
    if new_status not in (Service_Call_Status.COMPLETED, Service_Call_Status.FAILED, Service_Call_Status.IN_PROGRESS):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be in progress, complete or failed",
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


@router.patch("/{service_call_id}/priority", response_model=ServiceCallRead, status_code=status.HTTP_202_ACCEPTED)
async def update_call_priority(
    service_call_id: int,
    new_priority: Service_Call_Priority = Query(...),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(Technician_RBAC.OPERATION_MANAGER)),
) -> ServiceCall:
    service_call = await db.get(ServiceCall, service_call_id)
    if service_call is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service call with {service_call_id} not found",
        )

    service_call.priority = new_priority
    await db.commit()
    await db.refresh(service_call)
    return service_call

#-----------------------------------------------------------------------------------
