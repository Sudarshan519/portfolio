from typing import Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from apps.rps_remit.kyc.schema import *
from apps.rps_remit.kyc_state.schema import KycState, KycStateBase, KycStateRead 
from db.session_sqlmodel import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select

app=APIRouter(prefix='/ekycstate',tags=["REMIT EKYC STATE"] )
@app.get("/details")
async def details():
    return {"cards":CardType._member_names_}
@app.get('/',response_model=list[KycStateRead])
async def all(db:Session=Depends(get_session)):
    return Kyc.all(session=db)

@app.post('/')
async def create(hero:KycCreate,db:Session=Depends(get_session)):
    return KycState.create(hero,KycStateBase, db)

@app.get('/{id}',response_model=KycStateRead)
async def get_kyc(id:int,db:Session=Depends(get_session)):
    return KycState.by_id(id,session=db)


@app.patch('/{id}',response_model=KycStateRead)
async def update(id:int,hero:KycUpdate,db:Session=Depends(get_session)):
 
 
    return KycState.update(KycState.by_id(id,session=db),hero,db)
 
# @app.delete('/')
# async def delete(id:int,db:Session=Depends(get_session)):
#     return Kyc.delete(Kyc.by_id(id,session=db))