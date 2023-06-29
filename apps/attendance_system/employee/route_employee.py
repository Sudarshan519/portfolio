from fastapi import APIRouter

from apps.attendance_system.schemas.attendance import AttendanceTodayDetailModel
from db.models.attendance import Otp


router =APIRouter(include_in_schema=True,prefix='/api/v1/employee',tags=['Employee'])

@router.post('login')
async def login(phone:str):
    return {}
    # otp=Otp()
    # otp.setrand()
    # print(otp.code)
    # return {'otp':otp}


@router.get('companies')
async def get_companies():
    return {'companines':[],'inactive':[]}

@router.get('invitations')
async def get_invitations():
    return {"invitations":[]}

@router.post('attendance-store')
async def store_attendance():
    return {
        
    }
@router.post('start-break-submit')
async def store_break_start():

    return {}


@router.post('brek-end-submit')
async def store_break_end():
    return {}

@router.post('get-today-details',response_model=AttendanceTodayDetailModel)
async def get_today():
    return {}

