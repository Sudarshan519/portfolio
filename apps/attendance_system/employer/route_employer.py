 
from datetime import date, datetime, time, timedelta
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from requests import Session
from apps.attendance_system.route_login import get_current_user_from_token

from db.models.attendance import AttendanceUser,Otp,CompanyModel
from db.session import get_db


router =APIRouter(include_in_schema=True, tags=['Employer'])

@router.get('/companies')
async def get_companies():
    return {'companines':[],'inactive':[]}

class BaseAttendanceUser(BaseModel):
    phone:str
    otp:str

class Company(BaseModel):
    name:str
    addresss:str
    start_time:time
    stop_time:time
    established_date:date
    user_id:int
    established_tade:date



@router.post("/register",)#response_model = BaseAttendanceUser)
async def signup(phone:int,db: Session = Depends(get_db)):
 
    try:
        otp=Otp(phone=phone)
        otp.setrand()
        db.add(otp)
        db.commit()
        db.refresh(otp)
        print(otp.id)
        user=AttendanceUser(phone=phone,otp=otp.id)
        db.add(user)
        db.commit()
        # db.refresh(user)
        # print(user)
    except Exception as e:
        return {'error':f"{e}"}
 
    return BaseAttendanceUser(phone=phone,otp=otp.code)



@router.post('/verify')
def verify(otp:int,phone:int,db: Session = Depends(get_db),):
    user=db.query(AttendanceUser)
    try:
        tokens=None
        return {"token":tokens}
    except Exception as e:
        return {'error':f"{e}"}


# @router.post('/add-company')
# def add_company(company:Company,current_user: AttendanceUser = Depends(get_current_user_from_token)):
#     company_add=CompanyModel(**company.dict(),user_id=current_user.id)

