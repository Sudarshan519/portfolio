 
from typing import TYPE_CHECKING, List,Optional
 
from sqlmodel import Field, Relationship, SQLModel

 
from record_service.main import RecordService



if TYPE_CHECKING:
    from ..receiving_methods.schema import RecivingMethod
    from apps.rps_remit.user.schema import RemitUser

class RecipientBase(SQLModel):
    user_id:Optional[int]=Field(default=1, foreign_key="remituser.id",nullable=True)
    # 
    recipient_type:str
    recipient_country:str
    currency:str
    relationship:str
    title:str
    first_name:str
    last_name:str
    email:str
    mobile:str
    address:str
    note:str


class RecipientRead(RecipientBase):
    id:Optional[int] = Field(default=None, primary_key=True) 
 

class Recipient(RecipientBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 
    user_recipient: Optional["RemitUser"] = Relationship(back_populates="recipient")
    recivingmethod: List["RecivingMethod"] = Relationship(back_populates="recipient") 
    # transaction: List["Transaction"] = Relationship(back_populates="usertransaction")
class RecipientCreate(RecipientBase):
    pass
 
class RecipientUpdate(RecipientBase):
    pass

