from typing import Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from apps.rps_remit.remit_banks.schema import *
from db.session_sqlmodel import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select
# from ..currency_router import app as currencyapp

app=APIRouter(prefix='/nepal-bank',tags=["REMIT NEPAL BANK"] )

@app.get('/',response_model=list[NepalBankRead])
async def all(db:Session=Depends(get_session)):
    return NepalBank.all(session=db)

@app.post('/')
async def create(hero:NepalBankCreate,db:Session=Depends(get_session)):
    return NepalBank.create(hero,NepalBankBase, db)

@app.get('/{id}',response_model=NepalBankRead)
async def get_hero(id:int,db:Session=Depends(get_session)):
    return NepalBank.by_id(id,session=db)


@app.patch('/{id}',response_model=NepalBankRead)
async def update(id:int,hero:NepalBankUpdate,db:Session=Depends(get_session)):
 
 
    return NepalBank.update(NepalBank.by_id(id,session=db),hero,db)
 
@app.delete('/')
async def delete(id:int,db:Session=Depends(get_session)):
    return NepalBank.delete(NepalBank.by_id(id,session=db))