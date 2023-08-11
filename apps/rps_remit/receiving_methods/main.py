from typing import Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from pydantic import BaseModel 
from apps.rps_remit.recipient.schema import * 
from db.session_sqlmodel import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select
from ..receiving_methods.schema import RecivingMethodBase, RecivingMethodRead, RecivingMethodUpdate
app=APIRouter(prefix='/recipient_method',tags=["REMIT RECIPIENT RECIVING METHOD"] )
class RecivingMethodResponse(BaseModel):
    RecivingMethod:RecivingMethodRead
    recivingMethods:List[RecivingMethodRead]
@app.get('/',response_model=list[RecivingMethodResponse])
async def all(db:Session=Depends(get_session)):
    return RecivingMethod.all(session=db)

@app.post('/')
async def create(hero:RecivingMethodUpdate,db:Session=Depends(get_session)):
    print(hero)
    return RecivingMethod.create(hero,RecivingMethodBase, db)

@app.get('/{id}',response_model=RecivingMethodRead)
async def get_kyc(id:int,db:Session=Depends(get_session)):
    return RecivingMethod.by_id(id,session=db)


@app.patch('/{id}',response_model=RecivingMethodRead)
async def update(id:int,hero:RecivingMethodUpdate,db:Session=Depends(get_session)):
 
 
    return RecivingMethod.update(RecivingMethod.by_id(id,session=db),hero,db)
 
# @app.delete('/')
# async def delete(id:int,db:Session=Depends(get_session)):
#     return Kyc.delete(Kyc.by_id(id,session=db))