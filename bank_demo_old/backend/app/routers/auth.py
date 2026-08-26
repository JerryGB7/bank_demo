from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, require_role
from app.models import User, Technician_RBAC
from app.schemas.user import Token, UserCreate, UserRead
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

# defin our login endpoint, which will accept a username and password
# very the credentials, and return our JWT access if the credentials are valid

@router.post("/token", response_model=Token)
async def login(
    # use the OAuth2PasswordRequestForm dependency to extract the username and password
    # from the request body, Note this is sent as a form data, not JSON because of Depends()
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> Token:
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()


    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(f"UNAUTHORIZED")
        )

    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def registered_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(Technician_RBAC.OPERATION_MANAGER))
) -> User:
    existing = await db.execute(select(User).where(User.username == payload.username))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(f"Username {payload.username} is already taken"),
        )

    #create a new User Object
    user = User(
        username = payload.username, 
        hashed_password=hash_password(payload.password),
        role = payload.role
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user