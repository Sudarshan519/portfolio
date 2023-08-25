from fastapi import APIRouter, Depends
from requests import Session, session
from apps.rps_remit.remit_pickup_locations.schema import *

from db.session_sqlmodel import get_session


app=APIRouter(prefix='/cash-pickup-locations',tags=["REMIT Cash Pickup"] )



# @app.post('/add_recipient')
# async def add_recipient(recipient:CashPickupCreate,recivingMethod:RecivingMethodCreate , db:session=Depends(get_session)):
#     recipient= CashPickup.create(recipient,CashPickupBase, db)
#     recivingMethod.recipient_id=recipient.id
#     create_recivingMethod(recivingMethod,db)
#     return Recipient.by_id(recipient.id,db)

@app.get('/',response_model=list[CashPickup])
async def all(db:Session=Depends(get_session)):
    return CashPickup.all(session=db)

@app.post('/')
async def create(bankdeposit:CashPickupCreate,db:Session=Depends(get_session)):
    print(bankdeposit)
    return CashPickup.create(bankdeposit,CashPickUpBase, db)

@app.get('/{id}',response_model=CashPickupRead)
async def get_bank_deposit(id:int,db:Session=Depends(get_session)):
    return CashPickup.by_id(id,session=db)


@app.patch('/{id}',response_model=CashPickupRead)
async def update(id:int,hero:CashPickupUpdate,db:Session=Depends(get_session)):
 
 
    return CashPickup.update(CashPickup.by_id(id,session=db),hero,db)
 
@app.delete('/')
async def delete(id:int,db:Session=Depends(get_session)):
    return CashPickup.delete(CashPickup.by_id(id,session=db))