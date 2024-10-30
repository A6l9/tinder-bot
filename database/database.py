from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr
from config.config import POSTGRES_DB, POSTGRES_PASSWORD, HOST, PORT, POSTGRES_USER


DB_HOST = HOST
DB_PORT = PORT
DB_NAME = POSTGRES_DB
DB_USER = POSTGRES_USER
DB_PASSWORD = POSTGRES_PASSWORD

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
