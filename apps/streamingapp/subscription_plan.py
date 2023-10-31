from typing import Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from apps.streamingapp.schema import *
from db.session_sqlmodel import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select
# from ..currency_router import app as currencyapp

app=APIRouter(prefix='/subscriptionplan',tags=["REMIT PLAN"] )

@app.get('/',response_model=list[SubscriptionPlanRead])
async def all(db:Session=Depends(get_session)):
    return SubscriptionPlan.all(session=db)

@app.post('/')
async def create(hero:SubscriptionPlanCreate,db:Session=Depends(get_session)):
    return SubscriptionPlan.create(hero,SubscriptionPlanBase, db)

@app.get('/{id}',response_model=SubscriptionPlanRead)
async def get_hero(id:int,db:Session=Depends(get_session)):
    return SubscriptionPlan.by_id(id,session=db)


@app.patch('/{id}',response_model=SubscriptionPlanRead)
async def update(id:int,hero:SubscriptionPlanUpdate,db:Session=Depends(get_session)):
 
 
    return SubscriptionPlan.update(SubscriptionPlan.by_id(id,session=db),hero,db)
 
@app.delete('/{id}')
async def delete(id:int,db:Session=Depends(get_session)):
    return SubscriptionPlan.delete(SubscriptionPlan.by_id(id,session=db))