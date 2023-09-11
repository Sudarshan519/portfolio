from fastapi import APIRouter, Depends
from requests import Session, session

from apps.rps_remit.coupon.schema import *
from db.session_sqlmodel import get_session


app=APIRouter(prefix='/coupon',tags=["REMIT COUPON"] )


@app.get('/',response_model=list[CouponRead])
async def all(db:session=Depends(get_session)):
    return Coupon.all(session=db)

@app.post('/')
async def create(hero:CouponCreate=Depends(),db:Session=Depends(get_session)):
    return Coupon.create(hero,CouponBase, db)

@app.get('/{id}',response_model=CouponRead)
async def get_transaction(id:int,db:Session=Depends(get_session)):
    return Coupon.by_id(id,session=db)


@app.patch('/{id}',response_model=CouponRead)
async def update(id:int,hero:CouponCreate=Depends(),db:Session=Depends(get_session)):
    transaction=Coupon.by_id(id,session=db)
    status=hero.status
    user=Coupon.by_id(transaction.sender_id,db)
    # NotificationService.send_notification("Transaction Update",f"Your transaction has been {status}",user.fcm_token,  id, status)
    return Coupon.update(transaction,hero,db)
 
@app.delete('/')
async def delete(id:int,db:Session=Depends(get_session)):
    return Coupon.delete(Coupon.by_id(id,session=db))






from .use_coupon_main import app as usecoupon
app.include_router(usecoupon,prefix='')


