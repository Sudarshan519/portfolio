from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from record_service.main import RecordService
from db.session_sqlmodel  import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select

class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: Optional[int] = None

class HeroCreate(HeroBase):
    pass

class HeroRead(HeroBase):
    id:Optional[int] = Field(default=None, primary_key=True) 

class HeroUpdate(HeroBase):
    pass

 
class Hero(HeroBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 
