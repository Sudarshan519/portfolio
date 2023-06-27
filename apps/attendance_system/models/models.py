
from pydantic import BaseModel
from sqlalchemy import Column,Integer, String,Boolean, ForeignKey,Date,Time,Double
from sqlalchemy.orm import relationship


class CompanyModel(BaseModel):
    id = Column(Integer,primary_key=True,index=True)
    name:str
    start_time:Time
    end_time:Time
    established_date=Column(Date)
    desc=Column(String(1000))

class EmployeeModel(BaseModel):
    id = Column(Integer,primary_key=True,index=True)
    
    name:Column(str)
    login_time:Column(Time)
    logout_time:Column(Time)
    salary:Column(Double)
    duty_time:Column(Time)

    company_id =  Column(Integer,ForeignKey("companymodel.id",),default=1)
    company = relationship("CompanyModel",back_populates="companymodel")

class BreakModel(BaseModel):
    id = Column(Integer,primary_key=True,index=True)
    break_start=Column(Time)
    break_end=Column(Time)
class AttendanceModel(BaseModel):
    id = Column(Integer,primary_key=True,index=True)
    attendance_date=Column(Date)
    login_time:Column(Time)
    breaks:list[BreakModel]
    company_id =  Column(Integer,ForeignKey("companymodel.id",),default=1)
    employee_id=Column(Integer,ForeignKey("employeemodel.id",),default=1)
