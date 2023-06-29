 
from sqlalchemy import Column,Integer, String,Boolean, ForeignKey,Date,Time,Double
from sqlalchemy.orm import relationship
from db.base import Base

class Otp(Base):
    id=Column(Integer,primary_key=True,index=True)
    code=Column(str)
    phone=Column(Integer)
    created_at=Column(models.DateTimeField(_("created_at"), auto_now=True, auto_now_add=False))
    
    def setrand(self):
        self.code="{:04d}".format(random.randint(0, 9999))
    # def isvalid(self):
        # return 
class AttendanceUser(Base):
    id = Column(Integer,primary_key=True,index=True)
    phone=Column(Integer)
    photoUrl=Column(String,default='')
    name=Column(String,default='')
    
    
    
class CompanyModel(Base):
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
    company_id =  Column(Integer,ForeignKey("user.id",),default=1)
    company_id =  Column(Integer,ForeignKey("companymodel.id",),default=1)
    company = relationship("CompanyModel",back_populates="companymodel")

class BreakModel(BaseModel):
    id = Column(Integer,primary_key=True,index=True)
    break_start=Column(Time)
    break_end=Column(Time)
    company_id =  Column(Integer,ForeignKey("employeemodel.id",),default=1)
class AttendanceModel(BaseModel):
    id = Column(Integer,primary_key=True,index=True)
    attendance_date=Column(Date)
    login_time:Column(Time)
    breaks:list[BreakModel]
    company_id =  Column(Integer,ForeignKey("companymodel.id",),default=1)
    employee_id=Column(Integer,ForeignKey("employeemodel.id",),default=1)
