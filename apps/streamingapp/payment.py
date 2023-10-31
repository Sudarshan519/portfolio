from typing import Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from apps.streamingapp.schema.schema import *
from db.session_sqlmodel import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select
# from ..currency_router import app as currencyapp

app=APIRouter(prefix='/payment',tags=["REMIT STREAMING"] )

@app.get('/',response_model=list[PaymentRead])
async def all(db:Session=Depends(get_session)):
    return Payment.all(session=db)

@app.post('/')
async def create(hero:PaymentCreate,db:Session=Depends(get_session)):
    return Payment.create(hero,PaymentBase, db)

@app.get('/{id}',response_model=PaymentRead)
async def get_hero(id:int,db:Session=Depends(get_session)):
    return Payment.by_id(id,session=db)


@app.patch('/{id}',response_model=PaymentRead)
async def update(id:int,hero:PaymentUpdate,db:Session=Depends(get_session)):
 
 
    return Payment.update(Payment.by_id(id,session=db),hero,db)
 
@app.delete('/')
async def delete(id:int,db:Session=Depends(get_session)):
    return Payment.delete(Payment.by_id(id,session=db))