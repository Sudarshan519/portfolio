from typing import TYPE_CHECKING, List,Optional
# from pyparsing import Optional
from sqlmodel import Field, Relationship, SQLModel




from record_service.main import RecordService
from enum import Enum
class PaymentMode(str,Enum):
    CASH_PAYMENT="Cash Payment"
    Wallet="Wallet"
    BANK_DEPOSIT="Bank Deposit"
 

if TYPE_CHECKING:
    from apps.rps_remit.recipient.schema import Recipient
    from db.models.user import Transaction
class RecivingMethodBase(SQLModel):
    recipient_id:Optional[int]=Field(default=1, foreign_key="recipient.id",nullable=True)
    payment_mode:str="Cash Payment"#=PaymentMode.value#PaymentMode
    name:str=None
    account_number:str=None
    pickup_address:str=None

class RecivingMethodRead(RecivingMethodBase):
    id:Optional[int] = Field(default=None, primary_key=True) 


class RecivingMethod(RecivingMethodBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 
    recipient_recivingmethods:"Recipient" = Relationship(back_populates="recivingmethod") 
    recipient_transactions:"Transaction"=Relationship(back_populates="recivingMethod")
class RecivingMethodCreate(RecivingMethodBase):
    pass
 
class RecivingMethodUpdate(RecivingMethodBase):
    pass

 