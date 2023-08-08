import datetime
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from record_service.main import RecordService

class IndividualBusiness(BaseModel):
    title:str
    firstname:str
    middlename:str=None
    lastname:str
    nationality:str
    residence_type:str
    status_of_residence:str
    profession:str
    passport_number:str
    passport_image:str
    referal:str
    organization_type:str
    registered_business_name:str
    registration_number:str
    referal:str=None
