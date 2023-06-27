from typing import Optional
from pydantic import BaseModel,root_validator
from datetime import date,datetime,time

class BreakModel(BaseModel):
 
    break_start= (time)
    break_end= (time)
    class Config:
        schema_extra = {
            "example": {
        
                "start_date": "10:20",
                "end_date": "20:30",
           
            }
        }

class AttendanceModel(BaseModel):
    
    date_posted : Optional[date] = datetime.now().date()
    date_updated:Optional[date]=date
    attendance_date= (date)
    login_time: (date)
    breaks:list[BreakModel]
    company_id = int
    employee_id= int
