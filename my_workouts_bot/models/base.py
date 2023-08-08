from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from config.settings import POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_SERVER, POSTGRES_DB

DATABASE_URL_ASYNC = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL_ASYNC, pool_pre_ping=True, echo=True, echo_pool="debug", poolclass=NullPool) # Для дебага
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=True
)

