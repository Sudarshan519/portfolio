from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel
from apps.rps_remit.user.schema import RemitUser

from record_service.main import RecordService


class UserProfileBase(SQLModel):  
    user_id:Optional[int]=Field(default=1, foreign_key="remituser.id")  
    title: str 
    first_name: str 
    last_name: str 
    nationality: str 
    profile_type: str 
    status_of_residence: str 
    business_name: str =None
    business_registered_number: str =None
    passport_number: str =None
    referal_code: str =None
    profession: str =None
    residence_type: str =None
    organization_type:str =None
 
class UserProfileCreate(UserProfileBase):
    pass

class UserProfileRead(UserProfileBase):
    id:Optional[int] = Field(default=None, primary_key=True) 

class UserProfileUpdate(UserProfileBase):
    pass

 
class UserProfile(UserProfileBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 
    userprofile: List["RemitUser"] = Relationship(
        
            #    sa_relationship_kwargs={'uselist': True,'order_by':'UserProfile.index.desc()'},
       
        back_populates="profile")
    