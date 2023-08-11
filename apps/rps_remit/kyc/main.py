from typing import Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from apps.rps_remit.kyc.schema import * 
from db.session_sqlmodel import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select

app=APIRouter(prefix='/ekyc',tags=["REMIT EKYC"] )

@app.get('/',response_model=list[KycReadResp])
async def all(db:Session=Depends(get_session)):
    return Kyc.all(session=db)

@app.post('/')
async def create(hero:KycCreate,db:Session=Depends(get_session)):
    return Kyc.create(hero,KycBase, db)

@app.get('/{id}',response_model=KycRead)
async def get_kyc(id:int,db:Session=Depends(get_session)):
    return Kyc.by_id(id,session=db)


@app.patch('/{id}',response_model=KycRead)
async def update(id:int,hero:KycUpdate,db:Session=Depends(get_session)):
 
 
    return Kyc.update(Kyc.by_id(id,session=db),hero,db)
 
# @app.delete('/')
# async def delete(id:int,db:Session=Depends(get_session)):
#     return Kyc.delete(Kyc.by_id(id,session=db))