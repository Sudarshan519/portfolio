from fastapi import APIRouter

from apps.rps_remit.transactions_state.schema import *


app=APIRouter(prefix='/transaction-state',tags=["TRANSACTION STATE"] )

@app.get('/',response_model=list[TransactionStateRead])
async def all(db:Session=Depends(get_session)):
    return TransactionState.all(session=db)

@app.post('/')
async def create(hero:TransactionStateBase,db:Session=Depends(get_session)):
    return TransactionState.create(hero,TransactionStateBase, db)

@app.get('/{id}',response_model=TransactionStateRead)
async def get_hero(id:int,db:Session=Depends(get_session)):
    return TransactionState.by_id(id,session=db)


@app.patch('/{id}',response_model=TransactionStateRead)
async def update(id:int,hero:TransactionStateUpdate,db:Session=Depends(get_session)):
 
 
    return TransactionState.update(TransactionState.by_id(id,session=db),hero,db)
 
@app.delete('/')
async def delete(id:int,db:Session=Depends(get_session)):
    return TransactionState.delete(TransactionState.by_id(id,session=db))