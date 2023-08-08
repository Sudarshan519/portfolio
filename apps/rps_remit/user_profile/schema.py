from pydantic import BaseModel
from sqlmodel import SQLModel


class UserProfile(SQLModel):  
    user_id:str    
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
 