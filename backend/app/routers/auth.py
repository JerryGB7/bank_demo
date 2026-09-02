from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, require_role
from app.models import User, Technician_RBAC
from app.schemas.user import Token, UserCreate, UserRead
from app.security import create_access_token, hash_password, verify_password

# This router groups all authentication-related endpoints under the /auth prefix.
# It handles user login and account creation for the application.
router = APIRouter(prefix="/auth", tags=["auth"])

# -----------------------------------------------------------------------------
# Login endpoint:
# - Accepts username and password from the request form body.
# - Looks up the user in the database.
# - Verifies the submitted password against the stored hash.
# - If valid, creates and returns a JWT access token.
# -----------------------------------------------------------------------------
@router.post("/token", response_model=Token)
async def login(
    # OAuth2PasswordRequestForm reads the username and password from form data,
    # which is the standard format for OAuth2 password grant login requests.
    form_data: OAuth2PasswordRequestForm = Depends(),
    # get_db supplies the async database session for the query below.
    db: AsyncSession = Depends(get_db)
) -> Token:
    # Search for the matching user record by username.
    result = await db.execute(select(User).where(User.username == form_data.username.lower()))
    user = result.scalar_one_or_none()

    # Reject the login if the user is not found or the password is incorrect.
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # Build the JWT payload with the username and role.
    # This allows protected endpoints to identify the user and enforce permissions.
    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})

    # Return the token to the client in the standard bearer token format.
    return Token(access_token=access_token, token_type="bearer")


# -----------------------------------------------------------------------------
# Registration endpoint:
# - Allows an authorized operation manager to create a new user account.
# - Checks that the username is not already taken.
# - Hashes the password before saving it to the database.
# - Persists the new user and returns the created record.
# -----------------------------------------------------------------------------
@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def registered_user(
    # Incoming request payload contains the username, password, and role for the new user.
    payload: UserCreate,
    # Database session dependency allows the route to query and save user records.
    db: AsyncSession = Depends(get_db),
    # require_role ensures only OPERATION_MANAGER users can register new accounts.
    _: User = Depends(require_role(Technician_RBAC.OPERATION_MANAGER))
) -> User:
    # Check if this username already exists before creating a duplicate account.
    existing = await db.execute(select(User).where(User.username == payload.username.lower()))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username {payload.username} is already taken",
        )

    # Create a new User object from the incoming data.
    # Passwords are hashed before being stored so the database never keeps plain-text passwords.
    user = User(
        username=payload.username.lower(),
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )

    # Save the new user record and refresh it so the database session reflects the saved data.
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Return the created user object to the client.
    return user