from typing import Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from apps.rps_remit.remit_banks.schema import *
from db.session_sqlmodel import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select
# from ..currency_router import app as currencyapp

app=APIRouter(prefix='/japan-bank',tags=["REMIT JAPAN BANK"] )

@app.get('/',response_model=list[JapanBankRead])
async def all(db:Session=Depends(get_session)):
    return JapanBank.all(session=db)

@app.post('/')
async def create(hero:JapanBankCreate,db:Session=Depends(get_session)):
    return JapanBank.create(hero,JapanBankBase, db)

@app.get('/{id}',response_model=JapanBankRead)
async def get_hero(id:int,db:Session=Depends(get_session)):
    return JapanBank.by_id(id,session=db)


@app.patch('/{id}',response_model=JapanBankRead)
async def update(id:int,hero:JapanBankUpdate,db:Session=Depends(get_session)):
 
 
    return JapanBank.update(JapanBank.by_id(id,session=db),hero,db)
 
@app.delete('/')
async def delete(id:int,db:Session=Depends(get_session)):
    return JapanBank.delete(JapanBank.by_id(id,session=db))