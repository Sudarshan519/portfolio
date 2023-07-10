from typing import Optional,List
from pydantic import BaseModel,root_validator
from datetime import date,datetime,time


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
        # allow_population_by_field_name = True
        # arbitrary_types_allowed = True
        
        
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
class BreakStartModel(BaseModel):
    break_start_time:datetime
    user_id:int
class BreakEndModel(BaseModel):
    break_end_time:datetime
    user_id:int
class BreakModel(BaseModel):
    id:int
    break_start_time: (time)
    break_end_time: (time)
    class Config:
        schema_extra = {
            "example": {
                "break_start_time": "10:20",
                "break_end_time": "20:30"
            }
        }
        
class CompanyInvitation(BaseModel):
    employee:Employee
    company:Company
class AttendanceTodayDetailModel(BaseModel): 
    date_posted : Optional[date] = datetime.now().date()
    date_updated:Optional[date]=date
    id=Optional[int]
    attendance_date= (date)
    login_time: (datetime)
    logout_time:datetime
    breaks:List[BreakModel]
    company_id : int
    employee_id: int
    per_minute_salary: float
    class Config:
        arbitrary_types_allowed=True

class AttendanceBase(BaseModel): 
    date_posted : Optional[date] = datetime.now().date()
    date_updated:Optional[date]=date
    attendance_date= (date)
    attendance_id=int
    login_time: (datetime)
    logout_time:datetime
    breaks:List[BreakModel] 
