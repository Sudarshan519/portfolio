# from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Time,func, select
# from db.base import Base
# from sqlalchemy.orm import relationship

# class CompanyModel(Base):
#     id = Column(Integer,primary_key=True,index=True)
#     name=Column(String(256), unique=True)
#     address=Column(String(256))
#     start_time=Column(Time)
#     end_time=Column(Time)
#     established_date=Column(Date) 
#     is_active=Column(Boolean,default=True)
#     user_id =  Column(Integer,ForeignKey("attendanceuser.id",ondelete='CASCADE'),nullable=True)
#     employee=relationship("EmployeeModel",back_populates="company")
#     @property
#     def employee_count(self):
#         return len(self.attendance)

#     # @attendance_count.expression
#     def attendance_count(cls):
#         return (
#             select([func.count()])
#             .where(EmployeeModel.id == cls.id)
#             .label("attendance_count")
#         )