 
from datetime import date, datetime, time, timedelta
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile,status
from psycopg2 import IntegrityError
from pydantic import BaseModel, Field
from apps.attendance_system.route_login import get_current_user_from_token,get_current_user_from_bearer
from core.config import settings
from db.models.attendance import  AttendanceUser, EmployeeModel,Otp,CompanyModel
from requests import Session
from db.session import get_db
from fastapi import Depends, HTTPException, Request
from core.security import create_access_token
from typing import Optional
from db.repository.attendance_repo import AttendanceRepo
from week_util import getWeekDate
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
# {
#   "phone": "9863450107",
#   "otp": "0726"
# }eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5ODYzNDUwMTA3IiwiZXhwIjoxNjg4NjYxMzk3fQ.DGBN1ULWnN9db1_QMFLrQ4c8UmpZFqeEljuOtaIeatU
router =APIRouter(include_in_schema=True, tags=['Employer'])
import random
import json
@router.get('export-db')
async def export_db(db: Session = Depends(get_db)):
    data=AttendanceRepo.export_db(db)
    with open("exported_data.json", "w") as f:
        result=json.dump( (jsonable_encoder(data)),f)
    #     print(result)
    print(data)    
    
    return data
@router.get('/companies')
async def get_companies():
    return {'companines':[],'inactive':[]}

class BaseAttendanceUser(BaseModel):
    phone:str
    otp:str
    
class UpdateUser(BaseModel):
    name:str
    email:str
    dob:date
    class Config:
        orm_mode=True
        
class UpdatePhone(BaseModel):
    current_phone:int
    new_phone:int
    class Config:
        orm_mode=True
class AttendanceReport(BaseModel):
    name:str
    attendance_date:date
    login_time=time
    logout_time=time


class Company(BaseModel):
    name:str
    address:Optional[str]
    start_time:Optional[time]
    end_time:Optional[time]
    established_date:Optional[date] 
    class Config():  #to convert non dict obj to json
        schema_extra = {
            "example": { 
                    "name": "string",
                    "address": "string",
                    "start_time": "10:10",
                    "end_time": "10:30",
                    "established_date": "2023-06-30"
            }
        }
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        
        
class Employee(BaseModel):
    name:str
    login_time:time
    logout_time:time
    phone:int
    salary:float
    duty_time:time

    class Config():  #to convert non dict obj to json
        schema_extra={
            "example":{
  "name": "string",
  "login_time": "10:10",
  "logout_time": "10:10",
  "phone": 9800000000,
  "salary": 0,
  "duty_time": "10:50"
}
        }
        orm_mode = True

 
@router.get('/monthly-report')
async def getMonthlyReport(companyId,db:Session= Depends(get_db)):
    return AttendanceRepo.employeeWithAttendanceMonthlyReport(companyId,db)

@router.get("/today-report")
async def attendance(companyId:int, db: Session = Depends(get_db)):
 
        allAttendances=AttendanceRepo.todayReport(companyId,db)
        return allAttendances
 

@router.get("/weekly-report")
async def weeklyreport(companyId:int, db: Session = Depends(get_db)):
    dates= getWeekDate()
 
    weekdata=AttendanceRepo.getWeeklyAttendance(companyId,dates[0].date(),dates[1].date(), db)
 
    return weekdata
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


def create_user(phone,db,is_employer:bool=False):
    try:
        user=AttendanceUser(phone=phone,is_employer=is_employer)
        db.add(user)
        db.commit() 
        db.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=409, detail="This candidate alredy registered")
        raise HTTPException(status_code=400,detail=f'{e}')
    

def get_user(phone,db):
    user=db.query(AttendanceUser).filter(AttendanceUser.phone==phone).first()
    if not user:
        # return HTTPException(status_code=404,detail="User does not exist.")
        return None
    return user

def update_user(id:int,db,):
    try:
        
        pass
    except:
        pass
def create_company(user:AttendanceUser,db:Session,company:Company):
    try:
        # name=company.name,address=company.address,start_time=company.start_time,end_time=company.end_time,established_date=company.established_date
        new_company=CompanyModel(**company.dict(), user_id=user.id,is_active=True)
        db.add(new_company)
        db.commit()
        db.refresh(new_company)
 
        return new_company
    except Exception as e:
        return HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Company Name Already Registered.")

def companies_list(user:AttendanceUser,db:Session):

    try: 
        companies= db.query(CompanyModel).filter(CompanyModel.user_id==user.id).all()  
        return companies
    except Exception as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=e)

def create_employee(user:AttendanceUser,db:Session,employee:Employee,companyId:int):
    try:
         
        new_employee=EmployeeModel(**employee.dict(), user_id=user.id,company_id=companyId)
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee) 
        return new_employee

    except Exception as e:
        return HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Employee is already registered.{e}")

@router.post("/register",)#response_model = BaseAttendanceUser)
async def signup(phone:int,db: Session = Depends(get_db)):
    try:
        eixst_user=get_user(phone,db)
        if eixst_user==None:
            user=create_user(phone,db,is_employer=True ) 
        else:
            pass
        otp=create_otp(phone,db)
    except Exception as e:
        raise HTTPException(status_code=409, detail=f"This email alredy registered{e}")

 
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

 
@router.post('/add-company',)#response_model=Company
def add_company(company:Company,db: Session = Depends(get_db),current_user:AttendanceUser=Depends(get_current_user_from_bearer)): 
    company=create_company(current_user,db,company)
    return company

@router.post('/get-companies')
def all_companies(current_user:AttendanceUser=Depends(get_current_user_from_bearer),db: Session = Depends(get_db)):
    # print(current_user)
    company_list=AttendanceRepo.companies_list(user=current_user,db=db)
    
    return {"active":company_list}
posts=[]


@router.post('/add-employee')
def add_employee(employee:Employee,companyId:int, current_user:AttendanceUser=Depends(get_current_user_from_bearer),db: Session = Depends(get_db)):
    employee=create_employee(current_user,db,employee,companyId)
    return employee  

# @router.post('/add-employee')
# def add_employee(id:int,employee:Employee,companyId:int, current_user:AttendanceUser=Depends(get_current_user_from_bearer),db: Session = Depends(get_db)):
#     employee=AttendanceRepo.update_employee(id,db,employee,companyId)
#     return employee  


@router.post("/send-invitation")
def sendIntitation(employeeId,companyId,current_user:AttendanceUser=Depends(get_current_user_from_bearer),db: Session = Depends(get_db)):
    
    invitation=AttendanceRepo.create_company_invitation(employeeId,companyId,db)
    return invitation
def allemployees(id,db):
    return db.query(EmployeeModel).filter(EmployeeModel.company_id==id).all()
@router.get('/employee')
def all_employee(companyId:int, current_user:AttendanceUser=Depends(get_current_user_from_bearer),db: Session = Depends(get_db)):
    employeelist=allemployees(companyId,db)
    return employeelist
# @router.post("/posts",  tags=["posts"])#dependencies=[Depends(JWTBearer())],
# def add_post(post,current_user:AttendanceUser=Depends(get_current_user_from_bearer)):
#     print(current_user)
#     # post.id = len(posts) + 1
#     # posts.append(post.dict())
#     return {
#         "data": "post added."
#     }


import inspect
from typing import Type

from fastapi import Form
from pydantic import BaseModel
from pydantic.fields import ModelField

def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        model_field: ModelField  # type: ignore

        new_parameters.append(
             inspect.Parameter(
                 model_field.alias,
                 inspect.Parameter.POSITIONAL_ONLY,
                 default=Form(...) if model_field.required else Form(model_field.default),
                 annotation=model_field.outer_type_,
             )
         )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, 'as_form', as_form_func)
    return cls

@as_form
class FileUploadModel(BaseModel):
    name:list[str]
    # password:str=Field(None)
 
    # label:str=Field(...)
    uploadfile:list[UploadFile]

@router.post('/upload-files')
def upload(uploadfile:list[FileUploadModel]=Depends(FileUploadModel.as_form) ):
    return {}