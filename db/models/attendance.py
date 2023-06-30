 
from datetime import datetime,timedelta
from sqlalchemy import Column,Integer, String,Boolean, ForeignKey,Date,Time,Float,BigInteger,DateTime
from sqlalchemy.orm import relationship
from db.base import Base
import random
class Otp(Base):
    id=Column(Integer,primary_key=True,index=True)
    code=Column(String,nullable=False)
    phone=Column(BigInteger,nullable=False)
    created_at=Column(DateTime)  
    
    def setrand(self):
        self.code="{:04d}".format (random.randint(0, 9999))
        self.created_at=datetime.now()
    def isvalid(self):
        now:DateTime=datetime.now()
        return (now-self.created_at)<timedelta(minutes=2)
    

# class AttendanceUser(Base):
#     id = Column(Integer,primary_key=True,index=True)
#     phone=Column(Integer,unique=True)
#     photoUrl=Column(String,default='')
#     name=Column(String,default='')
#     otp = Column(Integer,ForeignKey('otp.id'))
 
    
class AttendanceUser(Base):
    id = Column(Integer,primary_key=True,index=True)
    phone=Column(BigInteger,unique=True,nullable=True,)
    photoUrl=Column(String,default='')
    name=Column(String,default='')
    is_verified=Column(Boolean,default=False)
    is_employer=Column(Boolean,default=False)
    is_approver=Column(Boolean,default=False)
    otp_id = Column(Integer,ForeignKey('otp.id'),nullable=True)

class CompanyModel(Base):
    id = Column(Integer,primary_key=True,index=True)
    name=Column(String, unique=True)
    address=Column(String)
    start_time=Column(Time)
    end_time=Column(Time)
    established_date=Column(Date) 
    is_active=Column(Boolean,default=False)
    user_id =  Column(Integer,ForeignKey("attendanceuser.id"),nullable=True)
     

class EmployeeModel(Base):
    id = Column(Integer,primary_key=True,index=True)
    phone=Column(BigInteger,unique=True)
    name=Column(String,nullable=False)
    login_time=Column(Time)
    logout_time=Column(Time)
    salary=Column(Float)
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
