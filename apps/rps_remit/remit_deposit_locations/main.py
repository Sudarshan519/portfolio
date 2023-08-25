from fastapi import APIRouter, Depends
from requests import Session, session
from apps.rps_remit.remit_deposit_locations.schema import *

from db.session_sqlmodel import get_session


app=APIRouter(prefix='/remit-deposit-locations',tags=["REMIT Deposit Locations"] )

@app.get('/',response_model=list[RemitDepost])
async def all(db:Session=Depends(get_session)):
    return RemitDepost.all(session=db)

@app.post('/')
async def create(bankdeposit:RemitDepostCreate,db:Session=Depends(get_session)):
    print(bankdeposit)
    return RemitDepost.create(bankdeposit,RemitDepostBase, db)

@app.get('/{id}',response_model=RemitDepostRead)
async def get_bank_deposit(id:int,db:Session=Depends(get_session)):
    return RemitDepost.by_id(id,session=db)


@app.patch('/{id}',response_model=RemitDepostRead)
async def update(id:int,hero:RemitDepostUpdate,db:Session=Depends(get_session)):
 
 
    return RemitDepost.update(RemitDepost.by_id(id,session=db),hero,db)
 
@app.delete('/')
async def delete(id:int,db:Session=Depends(get_session)):
    return RemitDepost.delete(RemitDepost.by_id(id,session=db))