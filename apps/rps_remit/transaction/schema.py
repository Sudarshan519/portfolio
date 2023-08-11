from datetime import date

from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel
from sqlmodel import Column, Enum, Field, Relationship, SQLModel
from .data_enums import *
from record_service.main import RecordService

    
if TYPE_CHECKING:
    from apps.rps_remit.user.main import RemitUser
class TransactionBase(SQLModel):
    sender_id:Optional[int]=Field(default=1, foreign_key="remituser.id")
    recipient_id:int=Field(foreign_key="recipient.id")#=1
    payment_mode:str="Cash Payment"
    reciving_method:int=Field(foreign_key="recivingmethod.id",default=1)#"Bank Deposit"#=
    closed_exchange_rate:float="1.01"
    amount_deposited:float="10000"
    source_of_fund:str="Business"
    service_charge:float="150"
    purpose:str="Travel"
    deposit_method:int=0#=Field(foreign_key="deposit_method")
    remarks:str="Payment for expenses."
    date_of_transfer:str
    status: TransactionStatus=TransactionStatus.INITIATED#str=Field(sa_column=Column(Enum(TransactionStatus)))


class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id:Optional[int] = Field(default=None, primary_key=True) 

class TransactionUpdate(SQLModel):
    status: TransactionStatus=TransactionStatus.VERIFIED

 
class Transaction(TransactionBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 
    usertransaction: Optional["RemitUser"] = Relationship(back_populates="transaction")