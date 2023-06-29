 
from datetime import datetime
from sqlalchemy import Column,Integer, String,Boolean, ForeignKey,Date,Time,Double
from sqlalchemy.orm import relationship
from db.base import Base
import random
class Otp(Base):
    id=Column(Integer,primary_key=True,index=True)
    code=Column(String,nullable=False)
    phone=Column(String,nullable=False)
    created_at=Column(Date)  
    
    def setrand(self):
        self.code="{:04d}".format (random.randint(0, 9999))
        self.created_at=datetime.now()
    def isvalid(self):
        return (datetime.now()-self.created_at)>180
    

# class AttendanceUser(Base):
#     id = Column(Integer,primary_key=True,index=True)
#     phone=Column(Integer,unique=True)
#     photoUrl=Column(String,default='')
#     name=Column(String,default='')
#     otp = Column(Integer,ForeignKey('otp.id'))
 
    
class AttendanceUser(Base):
    otp_id = Column(Integer,ForeignKey('otp.id'),nullable=True)
    id = Column(Integer,primary_key=True,index=True)
    phone=Column(Integer,unique=True,nullable=True)
    photoUrl=Column(String,default='')
    name=Column(String,default='')
    is_verified=Column(Boolean,default=False)

class CompanyModel(Base):
    user_id =  Column(Integer,ForeignKey("attendanceuser.id",),default=1)
    id = Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=True)
    start_time=Column(Time)
    address=Column(String)
    end_time=Column(Time)
    established_date=Column(Date)
    desc=Column(String(1000))
     

class EmployeeModel(Base):
    id = Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    login_time=Column(Time)
    logout_time=Column(Time)
    salary=Column(Double)
    duty_time=Column(Time)
    user_id =  Column(Integer,ForeignKey("attendanceuser.id",),default=1)
    company_id =  Column(Integer,ForeignKey("companymodel.id",),default=1)
    # company = relationship("companymodel",back_populates="companies")

class BreakModel(Base):
    id = Column(Integer,primary_key=True,index=True)
    break_start=Column(Time)
    break_end=Column(Time)
    company_id =  Column(Integer,ForeignKey("employeemodel.id",),default=1)

class AttendanceModel(Base):
    id = Column(Integer,primary_key=True,index=True)
    attendance_date=Column(Date)
    login_time=Column(Time)
    breaks= Column(Integer,ForeignKey('breakmodel.id'),default=1)
    company_id =  Column(Integer,ForeignKey("companymodel.id",),default=1)
    employee_id=Column(Integer,ForeignKey("employeemodel.id",),default=1)
