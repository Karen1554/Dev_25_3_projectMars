from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
## Asincronico
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRESQL_ADDON_USER_2")
DB_PASSWORD = os.getenv("POSTGRESQL_PASSWORD_2")
DB_HOST = os.getenv("POSTGRESQL_ADDON_HOST")
DB_PORT = os.getenv("POSTGRESQL_PORT_2")
DB_NAME = os.getenv("POSTGRESQL_ADDON_DB_2")

CLEVER_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

db_name = "pets1.sqlite3"
db_url = f"sqlite:///{db_name}"

engine_clever = create_async_engine(CLEVER_URL)

AsyncSessionLocal = async_sessionmaker(
    engine_clever,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    async with engine_clever.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


engine = create_engine(db_url)


def create_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


def get_session() -> Session:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
