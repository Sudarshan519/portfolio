from datetime import date
from enum import Enum
from sqlmodel import Column, Field, SQLModel
class CardType(str,Enum):
    RESIDENT_CARD="RESIDENT CARD"
    MY_NUMBER_CARD="MY NUMBER CARD"
    DRIVING_LICENSE="DRIVING LICENSE"

class TransactionStatus(str,Enum):
    INITIATED="INITIATED"
    PENDING="PENDING"
    VERIFIED="VERIFIED"
    CLOSED="CLOSED"
    CANCELED="CANCELED"

    
class TransactionBase(SQLModel):
    recipient_id:str=Field(foreign_key="recipient.id")
    payment_mode:str
    reciving_method:int=Field(foreign_key="reciving_methods.id")
    closed_exchange_rate:float
    amount_deposited:float
    source_of_fund:str
    service_charge:float
    purpose:str
    deposit_method:int=Field(foreign_key="deposit_method")
    remarks:str
    date_of_transfer:str
    status:Enum[TransactionStatus]=TransactionStatus.INITIATED#str=Field(sa_column=Column(Enum(TransactionStatus)))