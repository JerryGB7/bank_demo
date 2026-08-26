import asyncio

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import AsyncSessionLocal
from app.models import ATM, ATMStatus

async def atms_in_maintenance(session) -> list[ATM]:
    statement = (
        select(ATM).options(selectinload(ATM.branch)).where(ATM.status == ATMStatus.MAINTENANCE)
        .order_by(ATM.id)
    )

    result = await session.execute(statement)
    return list(result.scalars().all())

async def main() -> None:
    async with AsyncSessionLocal() as session:
        print("===Full atm registry===")
        all_atms_stmt = select(ATM).options(selectinload(ATM.branch)).order_by(ATM.id)

        all_atms = await session.execute(all_atms_stmt)
        for atm in all_atms.scalars():
            print(f"{atm}")

        print("\n === Robots in maintenance ===")
        alerts = await atms_in_maintenance(session)
        if not alerts:
            print("no atms in maintenance")
        for atm in alerts:
            print(f"ALERT: {atm.serial_number}")

if __name__ == "__main__":
    asyncio.run(main())