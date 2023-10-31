 
from fastapi import APIRouter, Depends 
from apps.streamingapp.schema.schema import *
from db.session_sqlmodel import get_session
from sqlmodel import Field, Session  

app=APIRouter(prefix='/user-subscription',tags=["REMIT SUBSCRIPTION"] )

@app.get('/',response_model=list[SubscriptionRead])
async def all(db:Session=Depends(get_session)):
    return Subscription.all(session=db)

@app.post('/')
async def create(hero:SubscriptionCreate,db:Session=Depends(get_session)):
    return Subscription.create(hero,SubscriptionBase, db)

@app.get('/{id}',response_model=SubscriptionRead)
async def get_hero(id:int,db:Session=Depends(get_session)):
    return Subscription.by_id(id,session=db)


@app.patch('/{id}',response_model=SubscriptionRead)
async def update(id:int,hero:SubscriptionUpdate,db:Session=Depends(get_session)):
 
 
    return Subscription.update(Subscription.by_id(id,session=db),hero,db)
 
@app.delete('/{id}')
async def delete(id:int,db:Session=Depends(get_session)):
    return Subscription.delete(Subscription.by_id(id,session=db))