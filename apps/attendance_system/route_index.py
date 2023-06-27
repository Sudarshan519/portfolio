from fastapi import APIRouter


router =APIRouter(include_in_schema=True)

from apps.attendance_system.schemas.company import CompanyBase
from apps.attendance_system.schemas.employee import EmployeeBase
from apps.attendance_system.schemas.attendance import AttendanceModel

@router.get('index',tags=[])
async def hello():
    return {"message":"Hello from attendance api"}

@router.post('add_company')
async def add_company(company:CompanyBase):
    return {"message":"Company added successfully."}

@router.post('add_employee')
async def add_employee(employee:EmployeeBase):
    return {"message":"Company added successfully."}

@router.post('add_attendance')
async def add_attendance(attendance:AttendanceModel):
    return {'message':"Addendance added successfully."}

