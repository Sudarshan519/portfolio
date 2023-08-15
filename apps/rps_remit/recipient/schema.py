 
from typing import TYPE_CHECKING, List,Optional
 
from sqlmodel import Field, Relationship, SQLModel

 
from record_service.main import RecordService



if TYPE_CHECKING:
    from ..receiving_methods.schema import RecivingMethod
    from apps.rps_remit.user.schema import RemitUser
    from apps.rps_remit.receiving_methods.schema import RecivingMethodRead


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
    is_quick_send:bool

class Recipient(RecipientBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 
    user_recipient: Optional["RemitUser"] = Relationship(back_populates="recipient")
    recivingmethod: List["RecivingMethod"] = Relationship(back_populates="recipient_recivingmethods" ) 
    @property
    def placeholder(self):
        return self.first_name[0]+self.last_name[0]
    # transaction: List["Transaction"] = Relationship(back_populates="usertransaction")
class RecipientRead(RecipientBase):
    id:Optional[int] = Field(default=None, primary_key=True) 
 


class RecipientCreate(RecipientBase):
    pass
 
class RecipientUpdate(RecipientBase):
    pass


from apps.rps_remit.receiving_methods.schema import RecivingMethod


class RecipientResponse(RecipientBase):
 
    recivingmethod:List[RecivingMethod] 