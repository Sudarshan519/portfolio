from fastapi import APIRouter, Depends
from pydantic import BaseModel
from apps.attendance_system.employee.route_employee import MissingAttendance
from apps.attendance_system.route_login import get_current_user_from_bearer
from db.models.attendance import AttendanceUser, EmployeeModel
from db.repository.attendance_repo import AttendanceRepo
from db.session import get_db
from requests import Session
from db.repository.attendance_repo import AttendanceRepo
from schemas.attendance import LeaveRequestStatusOut


class BaseAttendanceUser(BaseModel):
    phone:str
    otp:str


router =APIRouter(include_in_schema=True,prefix='',tags=['Approver'])


@router.post('/missing-attendance',)
async def add_missing_attendance( attendance:MissingAttendance, db: Session = Depends(get_db),):#current_user:AttendanceUser=Depends(get_current_user_from_bearer),):
    attendance=AttendanceRepo.missing_attendance(attendance,db)
    return attendance

class Employee(BaseModel):
    id:int
    name:str
    phone:str=None
    
    class Config:
        orm_mode=True

@router.get('/employees',response_model=list[Employee])
async def employees_list(companyId:int, db: Session = Depends(get_db)):#,current_user:AttendanceUser=Depends(get_current_user_from_bearer),):
    employees=db.query(EmployeeModel).filter(EmployeeModel.company_id==companyId,EmployeeModel.is_active==True).all()
    return employees


@router.get('/leave-request')
async def leaveRequests(companyId:int,db:Session=Depends(get_db)):
    return AttendanceRepo.leaveRequests(companyId,db)

@router.get('/update-request')
async def updateRequests(status:LeaveRequestStatusOut,companyId:int,db:Session=Depends(get_db)):
    return AttendanceRepo.updateRequests(status,companyId,db)
# @router.post('/')
# async def create_approver():
#     pass