"""run from the backend direcory with .venv enables using:
python -m scripts.day3_create_tables
"""

import asyncio

# Import the database engine configured for the app so this script can connect
# to the database and create the required schema.
from app.database import engine
# Import the SQLAlchemy declarative base that contains all mapped ORM models.
from app.models import Base


async def create_tables() -> None:
    """
    Create all tables defined by the app's SQLAlchemy models.

    This matters because simply defining model classes does not create database
    tables automatically. The database schema must exist before the application
    can insert, update, or query records.
    """
    # Open a database connection through the engine and start a transaction.
    async with engine.begin() as conn:
        # run_sync allows the synchronous SQLAlchemy metadata operation to run
        # inside the async database connection.
        # Base.metadata.create_all() inspects every model attached to Base and
        # creates any missing tables, constraints, and indexes in the database.
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    # Run the async setup function when this script is executed directly.
    # This is the standard pattern for initializing the database schema from a
    # command-line script during local development or setup.
    asyncio.run(create_tables())