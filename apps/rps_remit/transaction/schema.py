from datetime import date

from typing import Optional
from sqlmodel import Column, Enum, Field, SQLModel
from .data_enums import *
from record_service.main import RecordService

    
class TransactionBase(SQLModel):
    recipient_id:int#=Field(foreign_key="recipient.id")
    payment_mode:str
    reciving_method:int#=Field(foreign_key="reciving_methods.id")
    closed_exchange_rate:float
    amount_deposited:float
    source_of_fund:str
    service_charge:float
    purpose:str
    deposit_method:int=0#=Field(foreign_key="deposit_method")
    remarks:str
    date_of_transfer:str
    status: TransactionStatus=TransactionStatus.INITIATED#str=Field(sa_column=Column(Enum(TransactionStatus)))


class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id:Optional[int] = Field(default=None, primary_key=True) 

class TransactionUpdate(TransactionBase):
    pass

 
class Transaction(TransactionBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 
