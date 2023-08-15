
from fastapi import APIRouter, Depends

from apps.rps_remit.user.user_from_token import get_remit_user_from_bearer
 
from .schema import *
from db.session_sqlmodel import get_session
from sqlmodel import  Session  
app=APIRouter(prefix='/transactions',tags=["REMIT TRANSACTIONS"] )

@app.get('/',response_model=list[TransactionRead])
async def all(db:Session=Depends(get_session)):
    return Transaction.all(session=db)

@app.post('/')
async def create(hero:TransactionCreate=Depends(),db:Session=Depends(get_session)):
    return Transaction.create(hero,TransactionBase, db)

@app.get('/{id}',response_model=TransactionRead)
async def get_transaction(id:int,db:Session=Depends(get_session)):
    return Transaction.by_id(id,session=db)


@app.patch('/{id}',response_model=TransactionRead)
async def update(id:int,hero:TransactionUpdate=Depends(),db:Session=Depends(get_session)):
 
    print(hero)
    return Transaction.update(Transaction.by_id(id,session=db),hero,db)
 
@app.delete('/')
async def delete(id:int,db:Session=Depends(get_session)):
    return Transaction.delete(Transaction.by_id(id,session=db))


