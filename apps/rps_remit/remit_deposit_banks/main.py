from fastapi import APIRouter, Depends
from requests import Session, session
from apps.rps_remit.remit_deposit_banks.schema import *

from db.session_sqlmodel import get_session


app=APIRouter(prefix='/bank-deposit',tags=["REMIT BANK DEPOSIT"] )



# @app.post('/add_recipient')
# async def add_recipient(recipient:RemitBankDepositCreate,recivingMethod:RecivingMethodCreate , db:session=Depends(get_session)):
#     recipient= RemitBankDeposit.create(recipient,RemitBankDepositBase, db)
#     recivingMethod.recipient_id=recipient.id
#     create_recivingMethod(recivingMethod,db)
#     return Recipient.by_id(recipient.id,db)

@app.get('/',response_model=list[RemitBankDeposit])
async def all(db:Session=Depends(get_session)):
    return RemitBankDeposit.all(session=db)

@app.post('/')
async def create(bankdeposit:RemitBankDepositCreate,db:Session=Depends(get_session)):
    print(bankdeposit)
    return RemitBankDeposit.create(bankdeposit,RemitBankDepositBase, db)

@app.get('/{id}',response_model=RemitBankDepositRead)
async def get_bank_deposit(id:int,db:Session=Depends(get_session)):
    return RemitBankDeposit.by_id(id,session=db)


@app.patch('/{id}',response_model=RemitBankDepositRead)
async def update(id:int,hero:RemitBankDepositUpdate,db:Session=Depends(get_session)):
 
 
    return RemitBankDeposit.update(RemitBankDeposit.by_id(id,session=db),hero,db)
 
@app.delete('/')
async def delete(id:int,db:Session=Depends(get_session)):
    return RemitBankDeposit.delete(RemitBankDeposit.by_id(id,session=db))