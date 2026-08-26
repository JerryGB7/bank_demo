
from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.branch import Branch
from app.schemas.branch import BranchCreate, BranchRead



router = APIRouter(prefix="/branches", tags=["branches"])


@router.get("", response_model = list[BranchRead])
async def list_branches(db: AsyncSession = Depends(get_db)):

    statement = select(Branch)

    result = await db.execute(statement)

    return list(result.scalars().all())



@router.get("/{branch_id}", response_model=BranchRead)
async def get_branch(branch_id: int, db: AsyncSession = Depends(get_db)):
    branch = await db.get(Branch, branch_id)

    
    if branch is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"branch {branch_id} not found"
        )

    return branch


@router.post("", response_model=BranchRead, status_code=status.HTTP_201_CREATED)
async def create_branch(payload: BranchCreate, db: AsyncSession = Depends(get_db)):

    branch = Branch(**payload.model_dump())

    db.add(branch)
    await db.commit()
    await db.refresh(branch)
    return branch