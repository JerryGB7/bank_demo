from collections.abc import AsyncGenerator
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.models import User, Technician_RBAC
from app.security import decode_access_token

# This dependency opens a database session for each request and ensures the session is
# properly closed after the request completes. FastAPI dependencies can inject this
# session into route handlers and other dependencies, which is important for database
# queries that need to read or update application data in a request-scoped context.
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# FastAPI's OAuth2PasswordBearer reads the Authorization header and extracts the bearer
# token automatically. This is the mechanism by which incoming JWTs are passed into the
# rest of the authentication flow. The tokenUrl tells OpenAPI/Swagger where clients
# should request a token, which is useful for documenting the API.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# This dependency authenticates the caller by validating the JWT, extracting the user
# identity from its payload, and looking up that user in the database. This is a core
# security step because it prevents unauthenticated access and ensures the user exists
# before allowing access to protected routes.
async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
) -> User:
    # If authentication fails, we raise a 401 Unauthorized response. The
    # "WWW-Authenticate: Bearer" header tells the client the request must include a
    # bearer token, which is the standard way JWT-based APIs communicate auth errors.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}        
    )
    try:
        # decode_access_token is expected to verify the JWT signature and expiration, and
        # return the decoded payload. The JWT usually contains claims like "sub" (subject),
        # which represents the username or user ID. This step is critical because it
        # confirms the token is genuine and not tampered with.
        payload = decode_access_token(token)
        username = payload.get("sub")

        # If the token payload doesn't include a subject, we treat it as invalid because
        # the app cannot identify which user the token belongs to.
        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        # jwt.InvalidTokenError covers invalid signature, malformed token, expired token,
        # or other JWT validation problems. By catching it here, we convert raw token
        # failures into a clean API response instead of crashing the server.
        raise credentials_exception

    # Once the subject is identified, we query the database to ensure the user still
    # exists and has an active record. This prevents access based on a valid-looking token
    # for a deleted or disabled account.
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    
    return user

# This factory creates a dependency for protecting routes that require a specific role.
# It is useful for authorization boundaries such as admin-only, technician-only, or
# manager-only endpoints. By constructing the check as a dependency, FastAPI can reuse
# the same logic across many routes in a consistent and readable way.
def require_role(*allowed_roles: Technician_RBAC):
    # The inner function is itself a dependency. It depends on get_current_user, which
    # ensures the caller is authenticated before checking permissions. This order is
    # important: we first validate identity, then validate authorization.
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        # If the authenticated user's role is not in the allowed set for this route,
        # the API should return 403 Forbidden. This is different from 401 Unauthorized,
        # because the user is authenticated but not permitted for this action.
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(f"ACCESS DENIED - {current_user.role.value} is not permitted"),
        )
        # Returning the user allows the route handler to access the currently authenticated
        # user object without re-fetching it or repeating the permission check.
        return current_user
    return role_checker