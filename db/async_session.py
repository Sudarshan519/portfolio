from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlmodel import SQLModel

from core.config import settings
from typing import Generator            #new

SQLALCHEMY_DATABASE_URL = settings.SQLITE_URL
# SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
# SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL_PYTHON
# SQLALCHEMY_DATABASE_URL=settings.POSTGRES_URL


# engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread': False})#connect_args={'check_same_thread': False})
# engine = create_engine(SQLALCHEMY_DATABASE_URL,)
engine=AsyncEngine(create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread': False}))#connect_args={'check_same_thread': False}))
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
# Create an asynchronous session
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
from db import base
async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(base.Base.metadata.create_all)
        # await conn.run_sync(SQLModel.metadata.create_all)

async def get_db() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
# def get_db() -> Generator:   #new
#     try:
#         db =async_session# SessionLocal()
#         yield db
#     except:
#         pass
#     else:
#         pass
#     finally:
#         db.close()


async def commit_rollback():
    try:
        await get_db.commit()
    except Exception:
        await get_db.rollback()
        raise
db=SessionLocal()