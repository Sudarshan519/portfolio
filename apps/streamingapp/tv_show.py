from typing import Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from apps.streamingapp.schema.schema import *
from db.session_sqlmodel import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select
# from ..currency_router import app as currencyapp

app=APIRouter(prefix='/tvshow',tags=["REMIT TVShow"] )

@app.get('/',response_model=list[TVShowRead])
async def all(db:Session=Depends(get_session)):
    return TVShow.all(session=db)

@app.post('/')
async def create(hero:TVShowCreate,db:Session=Depends(get_session)):
    return TVShow.create(hero,TVShowBase, db)

@app.get('/{id}',response_model=TVShowRead)
async def get_hero(id:int,db:Session=Depends(get_session)):
    return TVShow.by_id(id,session=db)


@app.patch('/{id}',response_model=TVShowRead)
async def update(id:int,hero:TVShowUpdate,db:Session=Depends(get_session)):
 
 
    return TVShow.update(TVShow.by_id(id,session=db),hero,db)
 
@app.delete('/{id}')
async def delete(id:int,db:Session=Depends(get_session)):
    return TVShow.delete(TVShow.by_id(id,session=db))