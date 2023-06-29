from typing import Optional
from pydantic import BaseModel,root_validator
from datetime import date,datetime,time
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
        

class AttendanceTodayDetailModel(BaseModel): 
    date_posted : Optional[date] = datetime.now().date()
    date_updated:Optional[date]=date
    attendance_id=int
    attendance_date= (date)
    login_time: (datetime)
    logout_time:datetime
    breaks:list[BreakModel]
    company_id : int
    employee_id: int
    per_minute_salary: float
    
class AttendanceModel(BaseModel): 
    date_posted : Optional[date] = datetime.now().date()
    date_updated:Optional[date]=date
    attendance_date= (date)
    attendance_id=int
    login_time: (datetime)
    logout_time:datetime
    breaks:list[BreakModel] 
