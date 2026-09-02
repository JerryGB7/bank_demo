from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.atm import ATMRead, ATMCreate, DiscrepancyRead
from app.dependencies import get_db, get_current_user, require_role
from app.models import ATM, User, Technician_RBAC, Technician
from app.models.enums import ATMStatus

router = APIRouter(prefix="/atms", tags=["atms"])

#===============================================================
@router.get("", response_model = list[ATMRead])
async def list_atms(db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)):
    # need a way to interact with the db
    # we are dependent on the session object 
    # create our statement for the db
    statement = select(ATM).where(ATM.status != ATMStatus.OFFLINE)


    result = await db.execute(statement)
    return list(result.scalars().all())

# Low Cash Alert: Which active ATMs are operating below a 20% cash reserve across all branches?
@router.get("/low_cash", response_model = list[ATMRead])
async def active_atms_with_low_cash(low_cash_threshold: int = 20, db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)):

  # check for cash count
    statement = select(ATM).where(ATM.cash_level < low_cash_threshold).where(ATM.status != ATMStatus.OFFLINE)

    result = await db.execute(statement)
    return list(result.scalars().all())


# get a specific atm by its id
@router.get("/atm_id", response_model=ATMRead)
async def get_atm(atm_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)) -> ATM:
    atm = await db.get(ATM, atm_id)

    if atm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ATM with {atm_id} not found"
        )
    return atm

@router.get("/discrepency", response_model=list[DiscrepancyRead])
async def discrepency(db: AsyncSession = Depends(get_db)):
    statement = (
        select(
            ATM.id.label("ATM_id"),
            ATM.branch_id.label("ATM_branch_id"),
            ATM.technician_id.label("ATM_technician_id"),
            Technician.id.label("technician_id"),
            Technician.branch_id.label("technician_branch_id"),
        )
        .join(Technician, Technician.id == ATM.technician_id).where(Technician.branch_id != ATM.branch_id)
    )

    result = await db.execute(statement)
    return [dict(row) for row in result.mappings().all()]

#================================================================================================

# Post requests are used for creating new resources or altering state
@router.post("", response_model=ATMRead, status_code=status.HTTP_201_CREATED)
async def create_atm(payload: ATMCreate, db: AsyncSession = Depends(get_db), 
                     _: User=Depends(require_role(Technician_RBAC.OPERATION_MANAGER))):
   atm = ATM(**payload.model_dump())

   db.add(atm)
   await db.commit()
   await db.refresh(atm)
   return atm

@router.delete("/{atm_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_atm(atm_id: int, db: AsyncSession = Depends(get_db),
                     _: User = Depends(require_role(Technician_RBAC.OPERATION_MANAGER))):
    atm = await db.get(ATM, atm_id)
    if atm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ATM with {atm_id} not found"
        )

    await db.delete(atm)
    await db.commit()