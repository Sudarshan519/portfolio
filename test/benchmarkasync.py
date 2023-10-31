import time
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from core.config import settings
Base = declarative_base()

class Kyc(Base):
    __tablename__ = 'kyc'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)

DATABASE_URL = settings.EXTERNALPGURL#'sqlite+aiosqlite:///./test.db'  # Async SQLite database URL

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def async_create(session,user_id):
     
        kyc = Kyc(user_id=user_id)
        session.add(kyc)
        await session.commit()

# Define other asynchronous CRUD functions (read, update, delete) here


DATABASE_URL = settings.EXTERNALPGURL#'sqlite+aiosqlite:///./benchmarkasync.db'  # Async SQLite database URL

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def run_async_benchmark():
    await create_table()  # Create the table
    num_iterations = 1000

    total_async_create_time = 0

    for _ in range(num_iterations):
        # Measure asynchronous create time
        async def measure_async_create():
            async with async_session() as session:
                start_time = time.time()
                await async_create(session, "user123")
                end_time = time.time()
                return end_time - start_time

        total_async_create_time += await measure_async_create()

    avg_async_create_time = total_async_create_time / num_iterations

    print(f"Avg. Asynchronous Create Time: {avg_async_create_time:.6f} seconds")

if __name__ == "__main__":
    asyncio.run(run_async_benchmark())
