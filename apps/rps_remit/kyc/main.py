from typing import Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from apps.rps_remit.kyc.schema import *
from apps.rps_remit.user.user_from_token import get_remit_user_from_bearer 
from db.session_sqlmodel import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select

from other_apps.fcm_send import NotificationService

app=APIRouter(prefix='/ekyc',tags=["REMIT EKYC"] )

@app.get('/',response_model=list[KycReadResp])
async def all(db:Session=Depends(get_session)):
    return Kyc.all(session=db)

@app.post('/')
async def create(hero:KycCreate,current_user:RemitUser=Depends(get_remit_user_from_bearer),db:Session=Depends(get_session)):
    current_user.kyc_status=UserKycStatus.PENDING
    db.commit()

    return Kyc.create(hero,KycBase, db)

@app.get('/{id}',response_model=KycRead)
async def get_kyc(id:int,db:Session=Depends(get_session)):
    return Kyc.by_id(id,session=db)


@app.patch('/{id}',response_model=KycRead)
async def update(id:int,hero:KycUpdate,db:Session=Depends(get_session)):
 
 
    return Kyc.update(Kyc.by_id(id,session=db),hero,db)


@app.post('/verify-kyc',)
async def updateStatus(id:int,hero:KycStatusUpdate=Depends(),db:Session=Depends(get_session)):
    user=RemitUser.by_id(id,session=db)
    status=hero.kyc_status
    print(user.fcm_token)
    NotificationService.send_notification("Transaction Update",f"Your ekyc has been updated to {status}",user.fcm_token,  id, status)                   
    return RemitUser.update(user,hero,db)

# @app.delete('/')
# async def delete(id:int,db:Session=Depends(get_session)):
#     return Kyc.delete(Kyc.by_id(id,session=db))