from ast import List
from fastapi import Form, UploadFile
from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta
from typing import Any, Optional
from enum import Enum
import inspect
from typing import Type
from fastapi import Form
from pydantic import BaseModel
from pydantic.fields import ModelField

class RecivingMethod(str,Enum):
    BANK="Bank"
    CASH="CASH"
    WALLET="WALLET"
class BusinessLeaveDayType(str,Enum):
    SUNDAY='sun'
    MONDAY='mon'
    TUESDAY='tue'
    WEDNESDAY='wed'
    THURSDAY='thu'
    FRIDAY='fri'
    SATURDAY='sat'
class UserKycStatus(str,Enum):
    UNVERIFIED="UNVERIFIED"
    PENDING="PENDING"
    TEMPORARY="TEMPORARY"
    VERIFIED="VERIFIED"
    DOCUMENTEXPIRED="DOCUMENTEXPIRED"
    PREMIUM="PREMIUM"
def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        # print(model_field.field_info)
        model_field: ModelField  # type: ignore

        new_parameters.append(
             inspect.Parameter(
                 model_field.alias,
                 inspect.Parameter.POSITIONAL_ONLY,
                 default=Form(..., description= model_field.field_info.description if model_field.field_info else "") if model_field.required else Form(model_field.default),
                 annotation=model_field.outer_type_,
             )
         )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, 'as_form', as_form_func)
    return cls



class LeaveDayType(str,Enum):
    FULLDAY="FULLDAY"
    HALFDAY="HALFDAY"
class LeaveRequestType(str,Enum):
    # HOLIDAY="HOLIDAY"
    FESTIVAL="FESTIVAL"
    SICK="SICK"
    OTHER="OTHER"
class Status(str,Enum):
    INIT='INIT'
    INVITED="INVITED"
    ACCEPTED="ACCEPTED"
    REJECTED="REJECTED"
class StatusOut(str,Enum):
    ACCEPTED="ACCEPTED"
    REJECTED="REJECTED"

class LeaveRequestStatus(str,Enum):
    INIT='INIT' 
    ACCEPTED="ACCEPTED"
    REJECTED="REJECTED" 
class LeaveRequestStatusOut(str,Enum): 
    ACCEPTED="ACCEPTED"
    REJECTED="REJECTED"  
class AttendanceStatus(str,Enum):
    LATE="LATE"
    EARLY="EARLY"
    PRESENT="PRESENT"
    ABSENT="ABSENT"
    PENDING="PENDING"
    LEAVE="LEAVE"

@as_form
class LeaveRequestIn(BaseModel):
    employee_id:int=Field(default=1,title='Employee ID')
    start_date:date=Field(default='2022-02-22', description="eg.2022-02-22")
    end_date:date=Field(default='2022-02-22', description="eg.2022-02-22")
    leave_type:LeaveRequestType=LeaveRequestType.OTHER
    leave_day_type:LeaveDayType=LeaveDayType.FULLDAY
    
    remarks:str="Request For Leave"


class LeaveRequestOut(LeaveRequestIn):
    document:UploadFile=None
@as_form
class LeaveRequestList(BaseModel):
    data:LeaveRequestIn=[]
    # model_config = {
    #     "json_schema_extra": {
    #         "examples": 
    #             {
    #                 "start_date": "2022-02-22",
    #                 "description": "A very nice Item",
    #                 "price": 35.4,
    #                 "tax": 3.2,
    #             }
             
    #     }
    # }

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
    # user_id:int=None
    created_at:Optional[datetime]
    updated_at:Optional[datetime]
    total_casual_leave_in_year:int=10
    total_sick_leave_in_year:int=6
    
    class Config():  #to convert non dict obj to json
        # schema_extra = {
        #     "example": { 
        #             "name": "string",
        #             "address": "string",
        #             "start_time": "10:10",
        #             "end_time": "10:30",
        #             "established_date": "2023-06-30"
        #     }
        # }
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
class BusinessLeaveDays(BaseModel):
    day:str

class CompanyUpdate(BaseModel):
    name:str=None
    address:str=None
    start_time:Optional[time]
    end_time:Optional[time]
    established_date:Optional[date] 
    created_at:Optional[datetime]
    updated_at:Optional[datetime]
    total_casual_leave_in_year:int=10
    total_sick_leave_in_year:int=6
#     {
#   "name": "string",
#   "address": "string",
#   "established_date": "2023-08-22",
#   "created_at": "2023-08-22T15:43:52.888Z",
#   "updated_at": "2023-08-22T15:43:52.888Z",
#   "is_active": true
# }
       
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

class CompanyBase(BaseModel):
    id:int
    
    
    name:str=None
    address:str=None
    approver_count:int=None
    employee_count:int=None
    late:int=None
    inactive:int=None
    attendee:int=None

    # start_time:date=None
    # end_time:date=None
    established_date:Optional[date]
    created_at:Optional[date]
    updated_at:Optional[date]
    is_active:bool=None
    class Config:
        orm_mode=True

    # id = Column(Integer,primary_key=True,index=True)
    # name=Column(String(256), unique=True)
    # address=Column(String(256))
    # start_time=Column(Time)
    # end_time=Column(Time)
    # established_date=Column(Date) 
    # is_active=Column(Boolean,default=True)
    # user_id =  Column(Integer,ForeignKey("attendanceuser.id",ondelete='CASCADE'),nullable=True)
    # employee=relationship("EmployeeModel",back_populates="company",)
    # total_casual_leave_in_year=Column(Integer,default=18)
    # total_sick_leave_in_year=Column(Integer,default=6)
    # approver_count = column_property(select([func.count()]).where(id == EmployeeModel.company_id,EmployeeModel.is_approver==True)  # This part needs correction
    #     .label("approver_count")
    # )
    # employee_count = column_property(select([func.count()]).where(id == EmployeeModel.company_id)  # This part needs correction
    #     .label("employee_count")
    # )

class CompanyCreate(CompanyBase):
    businessleaveDays:list[str]=[]
    governmentleaveDates:list[date]=[]
    officialholiday:list[date]=[]
    class Config:
        orm_mode=True
class NotificationBase(BaseModel):
    # to:str
    user_id:int=1
    company_id:int=1
    title:str="Test Notification"
    desc:str="Testing Notification"
    subject:str="Adding Notification"
    