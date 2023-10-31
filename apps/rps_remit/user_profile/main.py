from typing import Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException

from apps.rps_remit.user.user_from_token import get_remit_user_from_bearer
from .schema import * 
from db.session_sqlmodel import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select

app=APIRouter(prefix='/signup-individual-business',tags=["REMIT INDIVIDUAL/BUSINESS"] )

@app.get('/',response_model=list[UserProfileRead])
async def all(db:Session=Depends(get_session)):
    return UserProfile.all(session=db)

@app.post('/')
async def create(hero:UserProfileCreate,db:Session=Depends(get_session),current_user:RemitUser=Depends(get_remit_user_from_bearer),):
    hero.user_id=current_user.id
    return UserProfile.create(hero,UserProfileBase, db)

@app.get('/{id}',response_model=UserProfileRead)
async def get_kyc(id:int,db:Session=Depends(get_session)):
    return UserProfile.by_id(id,session=db)


@app.patch('/{id}',response_model=UserProfileRead)
async def update(id:int,hero:UserProfileUpdate,db:Session=Depends(get_session)):
 
 
    return UserProfile.update(UserProfile.by_id(id,session=db),hero,db)
 
# @app.delete('/')
# async def delete(id:int,db:Session=Depends(get_session)):
#     return UserProfile.delete(UserProfile.by_id(id,session=db))