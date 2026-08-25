from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.atm import ATMRead, ATMCreate
from app.dependencies import get_db
from sqlalchemy import select
from app.models import ATM
from app.models.enums import ATMStatus

router = APIRouter(prefix="/atms", tags=["atms"])

@router.get("", response_model = list[ATMRead])
async def list_atms(
    cash_count: int | None = Query(
        default= None,
        ge=0,
        le=100,
        description="Returning ATMS with less than 20 percent cash level"
    ), db: AsyncSession = Depends(get_db)):
    # need a way to interact with the db
    # we are dependent on the session object 
    # create our statement for the db
    statement = select(ATM).where(ATM.status != ATMStatus.MAINTENANCE)

    # check for cash count
    if cash_count is not None:
     statement = statement.where(ATM.cash_level < cash_count)

    result = await db.execute(statement)
    return list(result.scalars().all())

# get a specific atm by its id
@router.get("/{atm_id}", response_model=ATMRead)
async def get_atm(atm_id: int, db: AsyncSession = Depends(get_db)) -> ATM:
    atm = await db.get(ATM, atm_id)

    if atm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ATM with {atm_id} not found"
        )
    return atm

# Post requests are used for creating new resources or altering state
@router.post("", response_model=ATMRead, status_code=status.HTTP_201_CREATED)
async def create_atm(payload: ATMCreate, db: AsyncSession = Depends(get_db)):
   atm = ATM(**payload.model_dump())

   db.add(atm)
   await db.commit()
   await db.refresh(atm)
   return atm