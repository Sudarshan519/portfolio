import json
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from record_service.main import RecordService
from db.session_sqlmodel  import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select

class CountryCurrencyBase(SQLModel):
    name: str
    currency: str
    flag:str=None
    @property
    def currency_list(self):
        return (self.currency).strip("][''").split(', ')
class CountryCurrencyCreate(CountryCurrencyBase):
    pass

class CountryCurrencyRead(CountryCurrencyBase):
    id:Optional[int] = Field(default=None, primary_key=True) 
class CountryRead(BaseModel):
    name: str
    # currency: str
    flag:str=None
    currency_list:list[str]
    class Config:
        orm_mode=True
class CountryCurrencyUpdate(CountryCurrencyBase):
    name: str 

 
class CountryCurrency(CountryCurrencyBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 
