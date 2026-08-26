import asyncio

from app.database import AsyncSessionLocal
from app.models import User, Technician_RBAC
from app.security import hash_password

async def seed_users() -> None:
    async with AsyncSessionLocal() as session:
        session.add_all([
            User(username="manager", hashed_password=hash_password("adminpass"), role=Technician_RBAC.OPERATION_MANAGER),
            User(username="technician", hashed_password=hash_password("workerpass"), role=Technician_RBAC.FIELD_TECHNICIAN),
            User(username="auditor", hashed_password=hash_password("auditorpass"), role= Technician_RBAC.AUDITOR)
        ])
        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed_users())