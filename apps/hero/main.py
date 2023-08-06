from typing import Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from apps.hero.schema import *
from db.session_sqlmodel import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select
from .currency_router import app as currencyapp

app=APIRouter(prefix='/hero',tags=['Hero' ])
app.include_router(currencyapp,prefix='/currency')

@app.get('/',response_model=list[HeroRead])
async def all(db:Session=Depends(get_session)):
    return Hero.all(session=db)

@app.post('/')
async def create(hero:HeroCreate,db:Session=Depends(get_session)):
    return Hero.create(hero,HeroBase, db)

@app.get('/{id}',response_model=HeroRead)
async def get_hero(id:int,db:Session=Depends(get_session)):
    return Hero.by_id(id,session=db)


@app.patch('/{id}',response_model=HeroRead)
async def update(id:int,hero:HeroUpdate,db:Session=Depends(get_session)):
    return Hero.update(Hero.by_id(id,session=db),hero,db)
 
@app.delete('/')
async def delete(id:int,db:Session=Depends(get_session)):
    return Hero.delete(Hero.by_id(id,session=db))