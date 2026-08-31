
# Import the FastAPI and SQLAlchemy pieces needed to define routes and interact with the database.
# These imports are important because the router depends on database access and request validation.
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.branch import Branch
from app.schemas.branch import BranchCreate, BranchRead


# This router groups all branch-related endpoints under the /branches URL prefix.
# The tag helps organize the API docs and makes the endpoint group easy to find.
router = APIRouter(prefix="/branches", tags=["branches"])


# List all branches in the database.
# The database session is a required dependency because every database query needs a live connection.
@router.get("", response_model=list[BranchRead])
async def list_branches(db: AsyncSession = Depends(get_db)):
    # Build a SELECT query for all Branch rows.
    statement = select(Branch)

    # Execute the query and return all matching Branch objects.
    result = await db.execute(statement)

    # The database returns rows; we convert them to a Python list for the API response.
    return list(result.scalars().all())


# Fetch one branch by its unique ID.
# The branch_id path parameter is important because it identifies the exact record the client wants.
@router.get("/{branch_id}", response_model=BranchRead)
async def get_branch(branch_id: int, db: AsyncSession = Depends(get_db)):
    # Look up the branch in the database using its primary key.
    branch = await db.get(Branch, branch_id)

    # If no record matches, raise a 404 so the client knows the resource does not exist.
    if branch is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"branch {branch_id} not found"
        )

    # Return the branch object if it exists.
    return branch


# Create a new branch record.
# The payload is important because it carries all the data the user is sending to create the branch.
@router.post("", response_model=BranchRead, status_code=status.HTTP_201_CREATED)
async def create_branch(payload: BranchCreate, db: AsyncSession = Depends(get_db)):
    # Convert the validated request body into a Branch model instance.
    branch = Branch(**payload.model_dump())

    # Add the new object to the session and commit it so it is persisted in the database.
    db.add(branch)
    await db.commit()
    await db.refresh(branch)

    # Return the created branch so the client receives the saved record.
    return branch