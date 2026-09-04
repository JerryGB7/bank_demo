import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from .config import settings

# Load the database connection string from the environment.

DATABASE_URL = settings.database_url 

# Create the asynchronous SQLAlchemy engine.
# The engine is the central object that manages database connections and
# connection pooling. It is built from the database URL and is used by all
# database operations in the app.
#
# 'echo=True' prints SQL statements to the console. This is very useful during
# development for debugging query issues, but it is usually disabled in production.
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory for async database access.
# async_sessionmaker produces database sessions for each operation. These sessions
# are bound to the engine and provide a clean way to manage transactions.
#
# 'expire_on_commit=False' keeps object attributes available after a commit,
# which is helpful in FastAPI apps when you want to return ORM objects after
# database operations without reloading them from the database.
#
# The AsyncSession type is imported to make the session type explicit in code,
# and to support IDE/static analysis when used elsewhere in the project.
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)