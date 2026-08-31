from collections.abc import AsyncGenerator
# AsyncGenerator is used as the return type for the database session dependency.
# It allows the function to yield an async SQLAlchemy session per request while
# preserving FastAPI's dependency lifecycle and ensuring the session is closed afterward.

import jwt
# PyJWT is used to validate JWT signatures and decode the access token.
# This is required in get_current_user() so the application can verify that the
# incoming bearer token is authentic and not expired or otherwise invalid.

from fastapi import Depends, HTTPException, status
# Depends is used by FastAPI to inject dependencies such as the database session or
# the authenticated user into route handlers.
# HTTPException is raised for authentication/authorization failures to return proper
# API error responses.
# status provides standard HTTP status codes like 401 Unauthorized and 403 Forbidden.

from fastapi.security import OAuth2PasswordBearer
# OAuth2PasswordBearer is the security scheme that extracts the bearer token from the
# Authorization header. It enables FastAPI to automatically parse JWTs sent by clients.

from sqlalchemy import select
# select is used to build SQLAlchemy queries to fetch the user record from the database
# based on the JWT subject claim. It is necessary for validating that the user still
# exists and is present in the app's database.

from sqlalchemy.ext.asyncio import AsyncSession
# AsyncSession is the async SQLAlchemy session type used for database operations in
# async FastAPI endpoints and dependencies. It provides request-scoped DB access that
# can be awaited without blocking the event loop.

from app.database import AsyncSessionLocal
# AsyncSessionLocal is the database engine/session factory used to open a new async
# database session for each request. This dependency is required to query the database
# while respecting SQLAlchemy async patterns and request-scoped cleanup.

from app.models import User, Technician_RBAC
# User is the application model representing authenticated users and is used to load
# the current user from the database after token validation.
# Technician_RBAC is the role enum used to enforce role-based access control on routes.
# These models are necessary for identity checks and permissions validation.

from app.security import decode_access_token
# decode_access_token is the custom JWT decoding helper that validates the token's
# signature and expiration. This is needed so get_current_user() can trust the token
# claims and extract the user's identity safely.

# This dependency opens a database session for each request and ensures the session is
# properly closed after the request completes. FastAPI dependencies can inject this
# session into route handlers and other dependencies, which is important for database
# queries that need to read or update application data in a request-scoped context.
# An async function can pause at await points without blocking other tasks, while a
# normal function runs synchronously and blocks until it returns.
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