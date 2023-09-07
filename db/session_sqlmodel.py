 
from typing import Generator   
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from core.config import settings
DATABASE_URL =settings.POSTGRES_URL# "sqlite:///db/database.db"#settings.DATABASE_URL## os.environ.get("DATABASE_URL")
# DATABASE_URL =settings.SQLITE_URL# "sqlite:///database.db"# os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL )#,connect_args={'check_same_thread': False})
# engine = create_engine(DATABASE_URL,)#connect_args={'check_same_thread': False,})
# engine = create_engine(DATABASE_URL,connect_args={'check_same_thread': False,})
# engine=AsyncEngine(create_engine(DATABASE_URL,connect_args={'check_same_thread': False}))
# "extend_existing":True
from sqlalchemy.orm import sessionmaker
def init_db():
    SQLModel.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)



def get_session() -> Generator:   #new
    try:
        db = SessionLocal()
        yield db
    except:
        pass
    else:
        pass
    finally:
        db.close()


async def commit_rollback():
    try:
        await get_session.commit()
    except Exception:
        await get_session.rollback()
        raise
db=SessionLocal()