 
from datetime import date, datetime, time, timedelta
from fastapi import APIRouter, Depends, HTTPException
from psycopg2 import IntegrityError
from pydantic import BaseModel
from requests import Session
from apps.attendance_system.route_login import get_current_user_from_token
from core.config import settings
from db.models.attendance import  AttendanceUser,Otp,CompanyModel
from db.session import get_db
from core.security import create_access_token
from fastapi import Depends, HTTPException, Request
 
router =APIRouter(include_in_schema=True, tags=['Employer'])
import random
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

@router.get('/users')#,response_model=list[AttendanceUser])
async def all_employers(db: Session = Depends(get_db)):
    return db.query(AttendanceUser).all()
def create_token(user,db):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.phone)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "Bearer"}

def create_otp(phone,db):
    otp=Otp(phone=phone)
    otp.setrand()
    db.add(otp)
    db.commit()
    db.refresh(otp)
    return otp
def create_user(phone,db):
    try:
        user=AttendanceUser(phone=phone)
        db.add(user)
        db.commit() 
        db.refresh(user)
        return user
    except Exception as e:
        return HTTPException(status_code=400,detail=f'{e}')
def get_user(phone,db):
    user=db.query(AttendanceUser).filter(AttendanceUser.phone==phone).first()
    if not user:
        return HTTPException(status_code=404,detail="User does not exist.")
    return user
@router.post("/register",)#response_model = BaseAttendanceUser)
async def signup(phone:int,db: Session = Depends(get_db)):
    try:
        eixst_user=get_user(phone,db)
        if not eixst_user:
            
            user=create_user(phone,db )
            # otp=create_otp(phone,db)
        else:
            pass
        otp=create_otp(phone,db)
    except Exception as e:
        raise HTTPException(status_code=409, detail=f"This email alredy registered{e}")
        return {'error':f"{e}"}
 
    return BaseAttendanceUser(phone=phone,otp=otp.code)

@router.post('/resend-otp')
async def resend_otp(phone:int,db: Session = Depends(get_db)):
    otp=create_otp(phone,db)
    return BaseAttendanceUser(phone=phone,otp=otp.code)

@router.post('/verify-otp')
def verify(code:str,phone:int,db: Session = Depends(get_db),):
    otp=db.query(Otp).filter(Otp.phone==phone).order_by(Otp.id.desc()).first()

    if otp is not None:
        user=db.query(AttendanceUser).filter(AttendanceUser.phone==phone).first()
        
        if otp.code==code:# and otp.isvalid():
            access_token=create_token(user,db)
            if user.is_verified:
                return access_token
            else:    
                user.is_verified=True
                db.commit()
            return access_token
        else:
            return HTTPException(status_code=401,detail=f"Otp does not match.")
    else:
        return HTTPException(status_code=404,detail=f"Otp not found for user {phone}")

 
@router.post('/add-company')
def add_company(company:Company,db: Session = Depends(get_db),current_user: AttendanceUser = Depends(get_current_user_from_token)):
    # print(user)
    return current_user
    # company_add=CompanyModel(**company.dict(),user_id=current_user.id)
from core.jwt_bearer import JWTBearer
posts=[]
@router.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
def add_post(post):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "data": "post added."
    }
