import asyncio

# Import the async database session factory used to talk to the database.
from app.database import AsyncSessionLocal
# Import the User model and role enum used by the RBAC system.
from app.models import User, Technician_RBAC
# Import the password-hashing helper so seeded users get securely stored hashes,
# not plain-text passwords in the database.
from app.security import hash_password

# This function seeds the database with a small set of default users used for
# testing and demonstration. It creates the required accounts at startup so the
# application can immediately authenticate and authorize users without manual setup.
async def seed_users() -> None:
    # Open an async database session. This ensures the inserts run in the same
    # transactional and async pattern used by the rest of the application.
    async with AsyncSessionLocal() as session:
        # Add multiple User records in one batch. Each record includes:
        # - a username that identifies the account
        # - a securely hashed password, so database storage is protected
        # - a role from the Technician_RBAC enum, which controls permissions and
        #   access to application features
        session.add_all([
            # Manager account: has operation-manager privileges, which usually means
            # they can oversee workflows, approve actions, and manage system-level
            # tasks in an RBAC-based application.
            User(username="manager", hashed_password=hash_password("adminpass"), role=Technician_RBAC.OPERATION_MANAGER),
            # Technician account: represents a field worker with operational access
            # to technician-specific tasks, while being restricted from manager-only
            # or auditor-only capabilities.
            User(username="technician", hashed_password=hash_password("workerpass"), role=Technician_RBAC.FIELD_TECHNICIAN),
            # Auditor account: used for review and compliance tasks. This role is
            # important for checking records, auditing actions, and verifying
            # process integrity without granting operational control.
            User(username="auditor", hashed_password=hash_password("auditorpass"), role=Technician_RBAC.AUDITOR)
        ])
        # Commit the transaction so the seeded records are saved to the database.
        # If this step is omitted, none of the new users would persist.
        await session.commit()

# This block allows the script to be run directly as a standalone utility.
# It is important because it makes the seeding process easy to execute for local
# development, testing, and database setup without needing to invoke the full app.
if __name__ == "__main__":
    # Start the async function and run it to completion.
    asyncio.run(seed_users())