from datetime import date
from enum import Enum
from typing import Optional,TYPE_CHECKING
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


from record_service.main import RecordService
from schemas.attendance import UserKycStatus

class CardType(str,Enum):
    RESIDENT_CARD="RESIDENT CARD"
    MY_NUMBER_CARD="MY NUMBER CARD"
    DRIVING_LICENSE="DRIVING LICENSE"

if TYPE_CHECKING:
    from apps.rps_remit.user.main import RemitUser
class KycBase(SQLModel):
    # team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    user_id:Optional[int]=Field(default=1, foreign_key="remituser.id")
    number:str
    type:str
    front_img:str=None
    back_img:str=None
    tilted_img:str=None
    selfie_img:str=None
    user_title:str=None
    first_name:str=None
    last_name:str=None
    dob:date
    nationality:str
    intended_use_of_account:str
    mobile_number:str
    phone_number:str=None
    gender:str
    date_of_issue:str=None
    peroid_of_stay:str
    expire_date:str
    postal:str
    prefecture:str
    city:str
    street_address:str=None
    building_name:str=None
    expiry_date:str=None
    annual_income:str=None
    source_of_income:str=None
    tax_return:str=None
    home_contact_number:str
    emergency_contact_number:str
    

    


    
class KycRead(KycBase):
    id:Optional[int] = Field(default=None, primary_key=True) 
from apps.rps_remit.user.schema import RemitUser, RemitUserRead

class Kyc(KycBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 
    user: Optional["RemitUser"] = Relationship(back_populates="kyc")


 
class KycCreate(KycBase):
    pass


class KycUpdate(KycBase):
    pass

     

# class KycReadResp(HeroRead):
#     team: Optional[TeamRead] = None


# class TeamReadWithHeroes(TeamRead):
#     heroes: List[HeroRead] = []



class UserBaseSchema(BaseModel):
    # name: str
    id:int
    email: str
    photo: str=None
    phone: str=None
    email_verified : bool=False
    phone_verified: bool=False
    kyc_status: str=None
    user_type:str=None
    # kyc:List[Kyc]=[]
    class Config:
        orm_mode = True

class KycReadResp(KycRead):
    user:UserBaseSchema=None 


class KycStatusUpdate(SQLModel):
    kyc_status: UserKycStatus=UserKycStatus.UNVERIFIED
