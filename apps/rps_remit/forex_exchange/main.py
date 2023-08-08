from fastapi import APIRouter, Depends
from requests import Session
from db.session_sqlmodel import get_session

from .schema import *


app=APIRouter(include_in_schema=True,prefix="/forex",tags=['FOREX'])
@app.get('/',response_model=list[ForexExchangeRead])
async def all(db:Session=Depends(get_session)):
    return ForexExchange.all(session=db)


@app.post('/')
async def create(hero:ForexExchangeCreate=Depends(),db:Session=Depends(get_session)):
    return ForexExchange.create(hero,ForeignExchangeChargeBase, db)

@app.get('/{id}',response_model=ForexExchangeRead)
async def get_exchange(id:int,db:Session=Depends(get_session)):
    return ForexExchange.by_id(id,session=db)


@app.patch('/{id}',response_model=ForexExchangeRead)
async def update(id:int,hero:ForexExchangeUpdate,db:Session=Depends(get_session)):
    # hero.updated_at = datetime.utcnow()
 
    return ForexExchange.update(ForexExchange.by_id(id,session=db),hero,db)
 
@app.delete('/')
async def delete(id:int,db:Session=Depends(get_session)):
    return ForexExchange.delete(ForexExchange.by_id(id,session=db))