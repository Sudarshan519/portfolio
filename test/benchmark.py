import time
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
from core.config import settings
class Kyc(Base):
    __tablename__ = 'kyc'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)


DATABASE_URL = settings.EXTERNALPGURL#'sqlite+aiosqlite:///./benchmark.db'  # SQLite database URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def sync_create(user_id):
    kyc = Kyc(user_id=user_id)
    session.add(kyc)
    session.commit()
# Define other asynchronous CRUD functions (read, update, delete) here


DATABASE_URL = 'sqlite:///./benchmarksync.db'  # SQLite database URL

engine = create_engine(DATABASE_URL,echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def sync_create(user_id):
    kyc = Kyc(user_id=user_id)
    session.add(kyc)
    session.commit()

def create_table():
    Base.metadata.create_all(engine)

def run_sync_benchmark():
    num_iterations = 1000

    total_sync_create_time = 0
    create_table()
    for _ in range(num_iterations):
        # Measure synchronous create time
        start_time = time.time()
        sync_create("user123")
        end_time = time.time()
        total_sync_create_time += (end_time - start_time)

    avg_sync_create_time = total_sync_create_time / num_iterations

    print(f"Avg. Synchronous Create Time: {avg_sync_create_time:.6f} seconds")

if __name__ == "__main__":
    run_sync_benchmark()
