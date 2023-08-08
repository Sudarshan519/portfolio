import json
from typing import Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException
 
from apps.rps_remit.currency.country_with_currency import *
from db.session_sqlmodel import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select

app=APIRouter(prefix='/currency',tags=['Currency' ])
def createNewCurrency(currency:CountryCurrencyCreate,db:Session=Depends(get_session)):
    print(currency.dict())
    f = open("myfile.json", "a")
    
    f.write(json.dumps(currency.dict())+"\n,")
    f.close()
    # CountryCurrency.create(currency,CountryCurrencyBase, db)
@app.get('/',response_model=list[CountryRead])
async def all(db:Session=Depends(get_session)):
    # f=open('myfile.json')
    # data=json.load(f)
    # for d in data:
    #     CountryCurrency.create(CountryCurrencyCreate(name=d['name'],currency=d['currency'],flag=d['flag']),CountryCurrencyBase,db)
    return CountryCurrency.all(session=db)

@app.post('/')
async def create(currency:CountryCurrencyCreate,db:Session=Depends(get_session)):
    return CountryCurrency.create(currency,CountryCurrencyBase, db)

@app.get('/{id}',response_model=CountryCurrencyRead)
async def get_currency(id:int,db:Session=Depends(get_session)):
    return CountryCurrency.by_id(id,session=db)


@app.patch('/{id}',response_model=CountryCurrencyRead)
async def update(id:int,hero:CountryCurrencyUpdate,db:Session=Depends(get_session)):
    return CountryCurrency.update(CountryCurrency.by_id(id,session=db),hero,db)
 
@app.delete('/')
async def delete(id:int,db:Session=Depends(get_session)):
    return CountryCurrency.delete(CountryCurrency.by_id(id,session=db))