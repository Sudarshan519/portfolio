import datetime
from typing import List, Optional,TYPE_CHECKING
from fastapi import Depends

from pydantic import BaseModel, EmailStr 
from sqlmodel import Field, Relationship, SQLModel,Column, Session,String,Boolean,Enum,Integer,ForeignKey, func, select
from sqlalchemy.orm import column_property


from apps.rps_remit.transaction.schema import Transaction
from db.session_sqlmodel import get_session 
 
from sqlalchemy.ext.hybrid import hybrid_property

from record_service.main import RecordService
from schemas.attendance import UserKycStatus 
from apps.rps_remit.recipient.schema import Recipient
if TYPE_CHECKING:
    from ..kyc.schema import Kyc
    from apps.rps_remit.user_profile.schema import UserProfile
    from apps.rps_remit.kyc_state.schema import KycState 
 

class RemitUserBase(SQLModel):
    # id: Column(Integer,primary_key=True,index=True)
    username :str=''# Column(String(60),unique=True,nullable=False)
    email :str
    phone:str=Field(default=None,sa_column=Column(String(16),nullable=True,)) 
    photo :str=''
    phone_verified:bool=False
    hashed_password: str
    is_active: bool=False
    verified:bool=False
    kyc_status:UserKycStatus=UserKycStatus.UNVERIFIED#=Field(sa_column=Column(Enum(UserKycStatus),nullable=True)) #Column(Enum(UserKycStatus),default=UserKycStatus.UNVERIFIED)
    kyc_verified:str=False
    # full_kyc=Column(Boolean,default=False)
    is_superuser: bool=False
    is_staff:bool=False
    role:str=''
    # document:int=Field(sa_column=Column(Integer,ForeignKey("Documents.id"),nullable=True))
    # kycType:int=Field(sa_column=Column(Integer,ForeignKey("Kyc.id"),nullable=True))
    # limit on transaction
    fcm_token:str=None
    total_limit:int=Field(sa_column=Column(Integer,default=0))
    per_day_limit:int=Field(sa_column=Column(Integer,default=0))
    per_month_limit:int=Field(sa_column=Column(Integer,default=0))
    per_year_limit:int=Field(sa_column=Column(Integer,default=0))
    # limit on amount
    per_day_amount:int=Field(sa_column=Column(Integer,default=0))
    per_month_amount:int=Field(sa_column=Column(Integer,default=0))
    per_year_amount:int=Field(sa_column=Column(Integer,default=0))

    refrence_id:int=None
    @property
    def email_verified(self):
        return self.verified

    
class RemitUserCreate(BaseModel):
    email: EmailStr 
    password : str

class RemitUserRead(RemitUserBase):
    id:Optional[int] = Field(default=None, primary_key=True) 

class RemitUserUpdate(RemitUserBase):
    pass
 
 
class RemitUser(RemitUserBase, RecordService, table=True):
 
    id:Optional[int] = Field(default=None, primary_key=True) 
    kyc: List["Kyc"] = Relationship(back_populates="user")
    profile: List["UserProfile"] = Relationship(back_populates="userprofile",
                                            # sa_relationship={
                                            #     'order_by':'UserProfile.index.desc()'
                                            # }
                                                )
    transaction: List["Transaction"] = Relationship(back_populates="usertransaction",sa_relationship_kwargs={
         "back_populates":"usertransaction",
        # "primaryjoin":"and_(Transaction.sender_id == RemitUser.id)",
        "order_by":"Transaction.id.desc()",
        # "lazy":"select",
        # "viewonly":"True",
        

    })
    recipient: List["Recipient"] = Relationship(back_populates="user_recipient",
                                             
                                                sa_relationship_kwargs={"order_by":"desc(Recipient.id)",
                                                                     
                                                                        })
    kycstate:List["KycState"]=Relationship(back_populates="user")
    # approver_count = column_property(select(Transaction).where(id == Transaction.sender_id).limit(4)  # This part needs correction
    #     .label("approver_count")
    # )
    # transactions=column_property(select(Transaction).where(id == Transaction.sender_id).limit(4))
    @property
    def transactions(self):
        return (
            self.transaction
            .limit(3)
            .all()
        )
    # @property
    # def transactions(self,db:Session=Depends(get_session)):
        
    #     # return Transaction.all(db) #self.db.query(select(Transaction).where(id == Transaction.sender_id).limit(4)).all() 
    #     return self.transaction[:3]
    # @hybrid_property
    # def filtered_children(self):
    #     return [child for child in self.children if child.name == "Child 1"]

    # @filtered_children.expression
    # def filtered_children(cls):
    #     return select(Recipient).filter(Recipient.is_quick_send == cls.id, ).all()

    @property
    def recipients(self, limit=20):
        return self.recipient[:limit]
    @property
    def quick_send(self):
        quickdata=[recipient for recipient in self.recipient if recipient.is_quick_send]
        return quickdata[:10] if len(quickdata)>=10 else quickdata
    @property
    def profile_setup(self):
        return True if self.profile!=[] else False
    @property
    def user_type(self):
        # return None
        return None if not self.profile else self.profile[-1].profile_type
     
        