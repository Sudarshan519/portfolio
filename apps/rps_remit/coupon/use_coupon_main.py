from fastapi import Depends
from fastapi.routing import APIRouter
from requests import Session

from apps.rps_remit.coupon.schema import *
from db.session_sqlmodel import get_session


app=APIRouter(prefix='/use-coupon',tags=["REMIT COUPON"] )
@app.get('/',response_model=list[UseCouponRead])
async def all(db:Session=Depends(get_session)):
    return UseCoupon.all(session=db)

@app.post('/')
async def create(hero:UseCouponCreate=Depends(),db:Session=Depends(get_session)):
    return UseCoupon.create(hero,UseCouponBase, db)

@app.get('/{id}',response_model=UseCouponRead)
async def get_transaction(id:int,db:Session=Depends(get_session)):
    return UseCoupon.by_id(id,session=db)


@app.patch('/{id}',response_model=UseCouponRead)
async def update(id:int,hero:UseCouponCreate=Depends(),db:Session=Depends(get_session)):
    transaction=UseCoupon.by_id(id,session=db)
    status=hero.status
    user=UseCoupon.by_id(transaction.sender_id,db)
    # NotificationService.send_notification("Transaction Update",f"Your transaction has been {status}",user.fcm_token,  id, status)
    return UseCoupon.update(transaction,hero,db)
 
@app.delete('/')
async def delete(id:int,db:Session=Depends(get_session)):
    return Coupon.delete(Coupon.by_id(id,session=db))
