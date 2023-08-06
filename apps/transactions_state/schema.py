from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from record_service.main import RecordService
from db.session_sqlmodel  import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select

class TransactionStateBase(SQLModel):
    name: str
    secret_name: str
    age: Optional[int] = None

class TransactionStateCreate(TransactionStateBase):
    pass

class TransactionStateRead(TransactionStateBase):
    id:Optional[int] = Field(default=None, primary_key=True) 

class TransactionStateUpdate(TransactionStateBase):
    name: str 

 
class TransactionState(TransactionStateBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 
