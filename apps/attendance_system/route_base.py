from fastapi import APIRouter


router =APIRouter(include_in_schema=True)

from apps.attendance_system.schemas.company import CompanyBase
from apps.attendance_system.schemas.employee import EmployeeBase
from apps.attendance_system.schemas.attendance import AttendanceTodayDetailModel

# @router.get('index',tags=[])
# async def hello():
#     return {"message":"Hello from attendance api"}

# @router.post('add_company')
# async def add_company(company:CompanyBase):
#     return {"message":"Company added successfully."}

# @router.post('add_employee')
# async def add_employee(employee:EmployeeBase):
#     return {"message":"Company added successfully."}

# @router.post('add_attendance',response_model=AttendanceModel)
# async def add_attendance():
#     return {'message':"Addendance added successfully."}
# @router.post('logout',response_model=AttendanceModel)
# async def add_logout():
    
#     return {'message':"Attendance updated"}

# @router.post('start_break',response_model=AttendanceModel)
# async def start_break():
#     return {'message':"Attendance updated"}

# @router.post('stop_break',response_model=AttendanceModel)
# async def stop_break():
#     return {'message':"Attendance updated"}

