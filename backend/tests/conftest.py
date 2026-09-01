import os 
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.dependencies import get_db
from app.main import app
from app.models import Base, Branch, User, Technician_RBAC
from app.security import create_access_token, hash_password

TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/bankdemo_test")
test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)

test_sessionmaker = async_sessionmaker(test_engine, expire_on_commit=False)

@pytest_asyncio.fixture
async def db_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_sessionmaker() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def seeded_user(db_session):
    users= {
        "admin": User(
            username="admin",
            password_hash=hash_password("adminpass"),
            role=Technician_RBAC.OPERATION_MANAGER,
        ),
        "technician": User(
            username="technician",
            password_hash=hash_password("techpass"),
            role=Technician_RBAC.FIELD_TECHNICIAN,
        ),
        "auditor": User(
            username="auditor",
            password_hash=hash_password("auditorpass"),
            role=Technician_RBAC.AUDITOR,
        )
    }
    for user in users.values():
        db_session.add(user)
    await db_session.commit()
    for user in users.values():
        await db_session.refresh(user)
    return users

@pytest_asyncio.fixture
async def seeded_branch(db_session):
    branch = Branch(name="Test Branch", location_region="Test Location", capacity=100, supervisor_id=1)
    db_session.add(branch)
    await db_session.commit()
    await db_session.refresh(branch)
    return branch

def auth_header(user: User) -> dict[str, str]:
    token = create_access_token({"sub": user.username, "role": user.role.value})
    return {"Authorization": f"Bearer {token}"}