from typing import TYPE_CHECKING, List,Optional
# from pyparsing import Optional
from sqlmodel import Field, Relationship, SQLModel



from record_service.main import RecordService

if TYPE_CHECKING:
    from apps.rps_remit.recipient.schema import Recipient
class RecivingMethodBase(SQLModel):
    recipient_id:Optional[int]=Field(default=1, foreign_key="recipient.id",nullable=True)
    payment_mode:str
    name:str=None
    account_number:str=None
    pickup_address:str=None

class RecivingMethodRead(RecivingMethodBase):
    id:Optional[int] = Field(default=None, primary_key=True) 


class RecivingMethod(RecivingMethodBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 
    recipient_recivingmethods:"Recipient" = Relationship(back_populates="recivingmethod") 

 
class RecivingMethodCreate(RecivingMethodBase):
    pass
 
class RecivingMethodUpdate(RecivingMethodBase):
    pass

 