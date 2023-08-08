from datetime import date
from enum import Enum
from sqlmodel import Field, SQLModel
class CardType(str,Enum):
    RESIDENT_CARD="RESIDENT CARD"
    MY_NUMBER_CARD="MY NUMBER CARD"
    DRIVING_LICENSE="DRIVING LICENSE"

class KycBase(SQLModel):
    user_id:Field(default=None, foreign_key="user.id")
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

    

    
