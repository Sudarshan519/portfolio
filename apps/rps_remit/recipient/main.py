from typing import Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from pydantic import BaseModel 
from apps.rps_remit.recipient.schema import * 
from db.session_sqlmodel import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select
from ..receiving_methods.schema import RecivingMethodRead
app=APIRouter(prefix='/recipient',tags=["REMIT RECIPIENT"] )

@app.get('/',response_model=list[RecipientResponse])
async def all(db:Session=Depends(get_session)):
    return Recipient.all(session=db)

@app.post('/')
async def create(hero:RecipientCreate,db:Session=Depends(get_session)):
    print(hero)
    return Recipient.create(hero,RecipientBase, db)

@app.get('/{id}',response_model=RecipientRead)
async def get_kyc(id:int,db:Session=Depends(get_session)):
    return Recipient.by_id(id,session=db)


@app.patch('/{id}',response_model=RecipientRead)
async def update(id:int,hero:RecipientUpdate,db:Session=Depends(get_session)):
 
 
    return Recipient.update(Recipient.by_id(id,session=db),hero,db)
 
# @app.delete('/')
# async def delete(id:int,db:Session=Depends(get_session)):
#     return Kyc.delete(Kyc.by_id(id,session=db))