from fastapi import APIRouter, Depends
from requests import Session
from db.session_sqlmodel import get_session

from .schema import *


app=APIRouter(include_in_schema=True,prefix="/forex",tags=['FOREX'])
@app.get('/charge-history',response_model=list[ForexExchangeRead])
async def all(db:Session=Depends(get_session)):
    return ForeignExchangeCharge.all(session=db)
@app.get('/',response_model=ForexExchangeRead)
async def service_charge(db:Session=Depends(get_session)):
    return ForeignExchangeCharge.latest(session=db)
    # return ForeignExchangeCharge.by_id(id=1, session=db)

@app.post('/')
async def create(hero:ForexExchangeCreate=Depends(),db:Session=Depends(get_session)):
    return ForeignExchangeCharge.create(hero,ForeignExchangeChargeBase, db)

@app.get('/{id}',response_model=ForexExchangeRead)
async def get_exchange(id:int,db:Session=Depends(get_session)):
    return ForeignExchangeCharge.by_id(id,session=db)


@app.patch('/{id}',response_model=ForexExchangeRead)
async def update(id:int,hero:ForexExchangeUpdate,db:Session=Depends(get_session)):
    # hero.updated_at = datetime.utcnow()
 
    return ForeignExchangeCharge.update(ForeignExchangeCharge.by_id(id,session=db),hero,db)
 
@app.delete('/')
async def delete(id:int,db:Session=Depends(get_session)):
    return ForeignExchangeCharge.delete(ForeignExchangeCharge.by_id(id,session=db))