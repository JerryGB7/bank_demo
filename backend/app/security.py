import os
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt

from .config import settings

# Secret key used to sign JWTs.
SECRET_KEY = settings.secret_key

# JWT signing algorithm. HS256 means the token is signed with a symmetric secret key,
# which is appropriate here because the same backend secret is used to both create and
# validate tokens. This keeps the implementation simple and secure as long as the secret
# remains private. If the secret were exposed, attackers could generate their own valid tokens.
ALGORITHM = "HS256"

# Default lifetime for access tokens. Short-lived tokens reduce the risk of stolen credentials
# being replayed for an extended period. This value is used if a caller does not pass an
# explicit expiration duration when creating a token.
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password management functions:
# - Hashing converts a plain-text password into a one-way representation that should not be
#   stored or logged in its original form.
# - Verification compares a plain-text password candidate with a stored hash without turning
#   the hash back into the original password.

# Hash a plain-text password using bcrypt. bcrypt is designed for password storage and is
# computationally expensive, which makes brute-force guessing much slower.
# Returning the hash as a UTF-8 string allows it to be safely stored in a database field.
def hash_password(plain_password: str) -> str:
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

# Verify a password by comparing a plain-text input against a stored bcrypt hash.
# This is important because the system should never check a password by comparing plain text
# directly to a stored password string. Instead, bcrypt recomputes the hash using the provided
# plain password and compares it against the stored hash in constant time.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

# Create a JWT access token containing user identity or other non-sensitive data.
# JWTs are useful for stateless authentication because the server can issue a signed token
# that the client sends on later requests, avoiding the need to keep session data in server
# memory. The token is signed so the server can verify it was not modified by a client.
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    # Work on a copy of the payload before adding claims so the original data is not mutated.
    # A JWT payload generally includes a user identifier and other claims like roles or scopes.
    to_encode = data.copy()

    # Set the expiration time in UTC. This is important because JWTs are time-based and should
    # be interpreted consistently across time zones. If a token is expired, the server should
    # reject it instead of allowing a client to continue using a stale credential.
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Decode and validate a JWT. This is the critical step for authentication: when the server
# receives a token, it verifies the signature and expiration before trusting any claims inside.
# If the token is invalid, expired, or tampered with, this will raise an exception and the
# request should be rejected.
def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
