from datetime import date

from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel
from sqlmodel import Column, Enum, Field, Relationship, SQLModel
from apps.rps_remit.receiving_methods.schema import PaymentMode

from schemas.attendance import RecivingMethod


from .data_enums import *
from record_service.main import RecordService
from apps.rps_remit.recipient.schema import Recipient
 
from sqlalchemy.orm import RelationshipProperty
if TYPE_CHECKING:
    from apps.rps_remit.user.main import RemitUser
    
class TransactionBase(SQLModel):
    sender_id:Optional[int]=Field(default=1, foreign_key="remituser.id")
    recipient_id:int=Field(foreign_key="recipient.id")#=1
    payment_mode:str="Bank Deposit"#PaymentMode #str="Cash Payment"
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


class TransactionUpdate(SQLModel):
    status: TransactionStatus=TransactionStatus.VERIFIED

 
class Transaction(TransactionBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 
    usertransaction: Optional["RemitUser"] = Relationship(back_populates="transaction")
    recipient: Optional["Recipient"] =Relationship(back_populates="transactions", sa_relationship_kwargs={"order_by":"desc(Recipient.id)"}) #back_populates="transactions",)# sa_relationship=RelationshipProperty(order_by='desc(Recipient.id)', lazy='dynamic'))
    # Relationship(back_populates="transactions", sa_relationship={"order_by":'desc(Recipient.id)', "lazy":'dynamic'})
    # reciving_method:RecivingMethod=Relationship(back_populates="recivingmethod")
    @property
    def recipient_name(self):
        # print(self.recipient.first_name)
        return self.recipient.first_name
    @property
    def country(self):
        return "NP" if self.recipient.recipient_country=="Nepal" else "Jp"
    @property
    def placeholder(self):
        return (self.recipient.first_name[0]+self.recipient.last_name[0]).upper()
class TransactionRead(TransactionBase):
    # recipient:Optional[Recipient]=None
    recipient_name:str=None
    country:str=None
    placeholder:str=None
    id:Optional[int] = Field(default=None, primary_key=True) 
    # recipient:Optional[Recipient]
    # reciving_method:RecivingMethod=None

# class TransactionWithRecipient(TransactionRead):
#     recipient:Optional[Recipient]=None