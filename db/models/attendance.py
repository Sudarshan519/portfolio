 
from datetime import date, datetime,timedelta
from sqlalchemy import Column,Integer, String,Boolean, ForeignKey,Date,Time,Float,BigInteger,DateTime,UniqueConstraint,Table,Enum,func, select
from sqlalchemy.orm import relationship,aliased
from db.base import Base
import random
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, column_property
from schemas.attendance import LeaveDayType, LeaveRequestStatus, LeaveRequestType, Status,AttendanceStatus
from fastapi import Depends
from requests import Session
from db.session import get_db
modelslist = Base.__subclasses__()
# Declare Classes / Tables
# employee_companies = Table('employee_companies', Base.metadata,
#     Column('employee_id', ForeignKey('employeemodel.id'), primary_key=True),
#     Column('company_id', ForeignKey('companymodel.id'), primary_key=True)
# )

class Otp(Base):
    id=Column(Integer,primary_key=True,index=True)
    code=Column(String(256),nullable=False)
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
#     photoUrl=Column(String(256),default='')
#     name=Column(String(256),default='')
#     otp = Column(Integer,ForeignKey('otp.id'))
 

class AttendanceUser(Base):
    id = Column(Integer,primary_key=True,index=True)
    phone=Column(BigInteger,unique=True,nullable=True,)
    photoUrl=Column(String(256) ,default='')
    name=Column(String(256),default='')
    email=Column(String(256),default='')
    is_verified=Column(Boolean,default=False)
    is_employer=Column(Boolean,default=False)
    is_approver=Column(Boolean,default=False)
    dob=Column(Date,nullable=True) 
    fcm_token=Column(String(256),nullable=True)

class AttendanceModel(Base):
    id = Column(Integer,primary_key=True,index=True)
    attendance_date=Column(Date)
    login_time=Column(Time,nullable=False)
    logout_time=Column(Time,nullable=True,)
    # breaks= Column(Integer,ForeignKey('breakmodel.id'),default=1)
    status=Column(Enum(AttendanceStatus),default=AttendanceStatus.PRESENT,)
    company_id =  Column(Integer,ForeignKey("companymodel.id",ondelete='CASCADE'),default=1)
    employee_id=Column(Integer,ForeignKey("employeemodel.id",ondelete='CASCADE'),default=1)
    breaks=relationship("BreakModel",back_populates='attendance')
    employee = relationship("EmployeeModel", back_populates="attendance")
    total_worked_seconds = column_property(
        func.coalesce(
            func.extract('epoch', logout_time) - func.extract('epoch', login_time),
            0
        )
    )
    @property
    def total_worked_hours_in_month(self):
        if not self.employee:
            return self.hours_worked_till_date

            
        else:
            return self.employee.total_worked_hours_in_month
    @total_worked_hours_in_month.setter
    def total_worked_hours_in_month(self,new):
        self.hours_worked_till_date=new
    @property
    def total_working_hours(self):
        if self.login_time is not None:
            if self.logout_time is not None:
                return (
                    (
                    self.logout_time.hour * 3600 +
                    self.logout_time.minute * 60 +
                    self.logout_time.second
                ) -
                (
                    self.login_time.hour * 3600 +
                    self.login_time.minute * 60 +
                    self.login_time.second
                ))
        return 0
        # (func.timestampdiff(func.SECOND, login_time, logout_time) / 3600).label('total_working_hours')

    def __init__(self, *args, **kwargs):
        self.salary=0#self.employee.salary
        self.approver=False
        self.hours_worked_till_date=0
        super().__init__(*args, **kwargs)
    @property
    def is_approver(self):
        if self.employee:
            return self.employee.is_approver or self.approver
        else:
            print("APPROVER")
            return self.approver
    @is_approver.setter
    def is_approver(self,new):
        self.approver=new
# GROUP BY, HAVING PLUS
    @property
    def hours_worked(self):
        if self.logout_time is not None:
            return calcTime(self.login_time,self.logout_time)/(60*60)
        return 4##calcTime(self.login_time+timedelta(hours=4))
    @property
    def salary(self):
        # print(self.employee.duty_time.minute)
        # print(self.employee.duty_time.hour)
        if not self.employee:
            return self.per_min_salary
        return  self.employee.salary/(30*(self.employee.duty_time.hour or 8)*self.employee.duty_time.minute)
    @salary.setter
    def salary(self,new):
        self.per_min_salary=new/(30*8*60)
    @property
    def duty_time(self):
        # Convert the time values to datetime.datetime objects using a fixed date (e.g., today's date)
        # date_today = datetime.date.today()
        # datetime1 = datetime.datetime.combine(date_today, self.employee.logout_time)
        # print(datetime1)
        # datetime2 = datetime.datetime.combine(date_today, self.employee.login_time)
 
        # # Calculate the time difference
        # time_diff = datetime2 - datetime1
        # print(time_diff)

        # # Extract the time difference as a timedelta object
        # duration = time_diff.total_seconds()

        # # Print the duration in seconds
        # print(duration)
        return self.employee.duty_time
        return calcTime(self.employee.login_time,self.employee.logout_time)
    
    @property
    def name(self):
        return self.employee.name
    
    __table_args__ = (
        UniqueConstraint('attendance_date', 'employee_id','company_id', name='uq_attendance_date_company_employee'),
    )
    # def breaks(self ,db: Session = Depends(get_db)):
    #     return db.query(BreakModel).filter(BreakModel.attendance==self.id).all()

class EmployeeModel(Base):
    id = Column(Integer,primary_key=True,index=True)
    phone=Column(BigInteger,unique=False)
    name=Column(String(256),nullable=False)
    login_time=Column(Time)
    logout_time=Column(Time)
    salary=Column(Float)
    duty_time=Column(Time)
    is_active=Column(Boolean,default=False)
    user_id =  Column(Integer,ForeignKey("attendanceuser.id",ondelete='CASCADE'),default=1)
    company_id =  Column(Integer,ForeignKey("companymodel.id",ondelete='CASCADE'),default=1)
    attendance = relationship("AttendanceModel", back_populates="employee")
    is_approver=Column(Boolean,default=False)

    # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5ODAwMDAwMDAwIiwiZXhwIjoxNjg4NDU2MTM1fQ.PeAR8N5yJ1Nn5wucM6hh9Pzmjc3ATwtScT_LBvc7mkw
    # status=Column(Enum(Status),default=False)
    status=Column(Enum(Status),default=Status.INIT,nullable=True)
    company=relationship("CompanyModel",back_populates="employee")
    total_sick_leave_taken=Column(Integer,default=0)
    total_casual_leave_taken=Column(Integer,default=0)
    
    # approver_count = column_property(select([func.count()]).where(id == EmployeeModel.company_id,EmployeeModel.is_approver==True)  # This part needs correction
    #     .label("approver_count")
    # )
    total_worked_hours_in_month = column_property((select([func.coalesce(func.sum(AttendanceModel.total_worked_seconds), 0)])
        .where(
                func.EXTRACT('year', AttendanceModel.attendance_date) == func.EXTRACT('year', func.current_date()),
                func.EXTRACT('month', AttendanceModel.attendance_date) == func.EXTRACT('month', func.current_date()),
                AttendanceModel.employee_id == id
            )
            .correlate_except(AttendanceModel)
            .as_scalar()
        ) / 3600
    )

    @property
    def available_sick_leave(self):
        if( self.company.total_sick_leave_in_year):
            return  self.company.total_sick_leave_in_year or 0-self.total_sick_leave_taken or 0
        else:
            return 0
    @property
    def available_casual_leave(self):
        return 0 #or self.company.total_casual_leave_in_year or 0-self.total_casual_leave_taken or 0
    @property
    def company_name(self):
        return self.company.name
    # def as_dict(self):
    #    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    __table_args__ = (
        UniqueConstraint('company_id','phone', name='uq_company_employee'),
    )


class CompanyModel(Base):
    id = Column(Integer,primary_key=True,index=True)
    name=Column(String(256), unique=True)
    address=Column(String(256))
    start_time=Column(Time)
    end_time=Column(Time)
    established_date=Column(Date,default=datetime.now) 
    created_at=Column(DateTime,default=datetime.now())
    updated_at=Column(DateTime,onupdate=datetime.now)
    is_active=Column(Boolean,default=True)
    user_id =  Column(Integer,ForeignKey("attendanceuser.id",ondelete='CASCADE'),nullable=True)
    employee=relationship("EmployeeModel",back_populates="company",)
    total_casual_leave_in_year=Column(Integer,default=18)
    total_sick_leave_in_year=Column(Integer,default=6)
    approver_count = column_property(select([func.count()]).where(id == EmployeeModel.company_id,EmployeeModel.is_approver==True)  # This part needs correction
        .label("approver_count")
    )
    employee_count = column_property(select([func.count()]).where(id == EmployeeModel.company_id)  # This part needs correction
        .label("employee_count")
    )
    
    attendee=column_property(select([func.count()])
            .where(AttendanceModel.company_id==id,AttendanceModel.attendance_date==date.today())
            .label("attendance_count"))
    inactive=column_property(select([func.count()])
            .where(EmployeeModel.company_id==id,EmployeeModel.status!=Status.ACCEPTED)
            .label("attendance_count"))
    late=column_property(select([func.count()])
            .where(AttendanceModel.company_id==id,AttendanceModel.attendance_date==date.today(),AttendanceModel.status==AttendanceStatus.LATE)
            .label("late"))
    # @property
    # def employee_count(self):
    #     return len(self.employee)
    # @property 
    # def last_three_employee(self):
    #     return 

    # @property
    # def approver_count(self):
    #     # worker_count = column_property(select([func.count(worker.id)]).filter(worker.project_id==id).scalar_subquery())
    #     data= select(([func.count(EmployeeModel.id)])
    #                   .filter(EmployeeModel.company_id==id).scalar_subquery()
    #                   )
    #     print(data)
    #     return data
    # @attendance_count.expression
    def attendance_count(cls):
        return (
            column_property(select([func.count()])
            .where(AttendanceModel.company_id==id,AttendanceModel.attendance_date==date.today())
            .label("attendance_count"))
        )
    
    

    
class BreakModel(Base):
    id = Column(Integer,primary_key=True,index=True)
    break_start=Column(Time)
    break_end=Column(Time)
    company_id =  Column(Integer,ForeignKey("employeemodel.id",ondelete='CASCADE'),default=1)
    attendance_id=Column(Integer,ForeignKey('attendancemodel.id',ondelete='CASCADE'), nullable=True )
    attendance=relationship("AttendanceModel",back_populates='breaks')
def calcTime(enter,exit):
    format="%H:%M:%S"
    #Parsing the time to str and taking only the hour,minute,second 
    #(without miliseconds)
    enterStr = str(enter).split(".")[0]
    exitStr = str(exit).split(".")[0]
    #Creating enter and exit time objects from str in the format (H:M:S)
    enterTime = datetime.strptime(enterStr, format)
    exitTime = datetime.strptime(exitStr, format)
    td=(exitTime-enterTime).total_seconds()
    return td

class EmployeeCompany(Base):
    id = Column(Integer,primary_key=True,index=True)
    employee_id=Column(Integer,ForeignKey('employeemodel.id',ondelete='CASCADE'),default=1)
    company_id=Column(Integer,ForeignKey('companymodel.id',ondelete='CASCADE'),default=1)
    is_invited=Column(Boolean,default=True)
    is_accepted=Column(Boolean,default=False)
    is_active=Column(Boolean,default=True)
    employee=relationship("EmployeeModel")#,back_populates="employeemodel")
    company=relationship("CompanyModel",)#back_populates="company")
    status=Column(Enum(Status),default=Status.INIT,nullable=True)
    # def company_name(self):
    #     print(self.company)
    #     return self.company.name
    # def company_start_time(self):
    #     return self.company.start_time
    # def company_end_time(self):
    #     return self.company.end_time
    # def established_date(self):
    #     return self.company.established_date
# class MonthlyReport(Base):
#     id = Column(Integer,primary_key=True,index=True)
#     employee_id=Column(Integer,ForeignKey('employeemodel.id',ondelete='CASCADE'),default=1)
#     employee=relationship("EmployeeModel",back_populates='monthly_report')
#     salary=Column(Float,default=0)
class LeaveRequest(Base):
    id = Column(Integer,primary_key=True,index=True)
    employee_id=Column(Integer,ForeignKey('employeemodel.id',ondelete='CASCADE'),default=1)
    company_id=Column(Integer,ForeignKey('companymodel.id',ondelete='CASCADE'),default=1)
    start_date=Column(Date)
    end_date=Column(Date,nullable=True)
    leave_type=Column(Enum(LeaveRequestType),nullable=True)
    leave_day_type=Column(Enum(LeaveDayType),nullable=True)
    document=Column(String(256),nullable=True)
    remarks=Column(String(256),nullable=True) 
    status=Column(Enum(LeaveRequestStatus),nullable=True,default=LeaveRequestStatus.INIT)
    # employee=relationship("EmployeeModel",back_populates='leave_report')

    # start_date:date
    # end_date:date
    # leaveType:LeaveRequestType
    # leaveDayType:LeaveDayType
    # doc:str
    # remarks:str


class Notifications(Base):
    id= Column(Integer,primary_key=True,index=True)
    to=Column(String(256),nullable=True)
    user_id=Column(Integer,ForeignKey('attendanceuser.id',ondelete='CASCADE'),default=1,nullable=True)
    company_id=Column(Integer,ForeignKey('companymodel.id',ondelete='CASCADE'),default=1,nullable=True)
    title=Column(String(256),nullable=True)
    desc=Column(String(256),nullable=True)
    # from:
    subject=Column(String(256),nullable=True)
    
    # data:

