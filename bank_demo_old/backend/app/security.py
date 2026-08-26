import os
from datetime import datetime, timedelta, timezone
import bcrypt 
import jwt

SECRET_KEY = os.environ.get("SECRET_KEY", "<replace-with-a-real-secret-key>")

# define our algorithm for signing our JWT(JSON web token) tokens
# There are many algorithms to choose from 
# we will use HS256 (this is a common choice for symmetric signing)
ALGORITHM = "HS256"

# expiration time for tokens in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# need two functions for password hashing and verification

# takes a plain text password as an input then hashes it using bcrypt
# returns the hash password as a string
def hash_password(plain_password: str) -> str:
    hashed =  bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

# takes a hashed password and a plain tet password as input
# checks if the plain and hashed passwords match
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

# function to create a JWT access token with the data and optional expiration time
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    # to encode is a copy of the input data dictionary, which will be used to create the payload of the JWT
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
