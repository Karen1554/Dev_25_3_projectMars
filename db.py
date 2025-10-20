from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
## Asincronico
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRESQL_ADDON_USER_2")
DB_PASSWORD = os.getenv("POSTGRESQL_ADDON_PASSWORD_2")
DB_HOST = os.getenv("POSTGRESQL_ADDON_HOST_2")
DB_PORT = os.getenv("POSTGRESQL_ADDON_PORT_2")
DB_NAME = os.getenv("POSTGRESQL_ADDON_DB_2")

CLEVER_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

)


db_name = "pets1.sqlite3"
db_url = f"sqlite:///{db_name}"

engine_clever :AsyncEngine = create_async_engine(CLEVER_URL, echo=True)

async_session = sessionmaker(engine_clever, expire_on_commit=False, class_=AsyncSession)

async def init_db(app: FastAPI):
    async with engine_clever.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session_clever():
    async with async_session() as session:
        yield session

##SQLITE
engine = create_engine(db_url)


def create_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


def get_session() -> Session:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[async_session, Depends(get_session_clever)]
