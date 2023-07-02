from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta
from typing import Optional
from enum import Enum
class Status(Enum):
    INIT='INIT'
    INVITED="INVITED"
    ACCEPTED="ACCEPTED"
    REJECTED="REJECTED"
class BaseAttendanceUser(BaseModel):
    phone:str
    otp:str
    
class UpdateUser(BaseModel):
    name:str
    email:str
    dob:date
    class Config:
        orm_mode=True
        
class UpdatePhone(BaseModel):
    current_phone:int
    new_phone:int
    class Config:
        orm_mode=True
        
class Company(BaseModel):
    name:str
    address:Optional[str]
    start_time:Optional[time]
    end_time:Optional[time]
    established_date:Optional[date] 
    class Config():  #to convert non dict obj to json
        schema_extra = {
            "example": { 
                    "name": "string",
                    "address": "string",
                    "start_time": "10:10",
                    "end_time": "10:30",
                    "established_date": "2023-06-30"
            }
        }
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

       
class Employee(BaseModel):
    name:str
    login_time:time
    logout_time:time
    phone:int
    salary:float
    duty_time:time

    class Config():  #to convert non dict obj to json
        schema_extra={
            "example":{
            "name": "string",
            "login_time": "10:10",
            "logout_time": "10:10",
            "phone": 9800000000,
            "salary": 0,
            "duty_time": "10:50"
            }
        }
        orm_mode = True