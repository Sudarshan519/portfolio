 
from datetime import date, datetime, time, timedelta
from fastapi import APIRouter, Body, Depends, File, Form, HTTPException, UploadFile,status
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
from schemas.attendance import Status
from week_util import getWeekDate
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
# 9863450107
# 0689
# {
#   "phone": "9863450107",
#   "otp": "0726"
# }eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5ODYzNDUwMTA3IiwiZXhwIjoxNjg4NjYxMzk3fQ.DGBN1ULWnN9db1_QMFLrQ4c8UmpZFqeEljuOtaIeatU
router =APIRouter(prefix='/api/v1', include_in_schema=True, tags=[])
import random
import json

@router.get('/import-db',tags=['Import/Export'])
async def import_db(db: Session = Depends(get_db)):
 
    with open("exported_data.json", "r") as f:
        result=json.load(f)
        # print(result)
    if result is None:
        return {}
    else:
        data=AttendanceRepo.import_db_from_json(result,db)
    #     print(result)
    print(data)    
    
    return data

@router.get('/export-db',tags=['Import/Export'])
async def export_db(db: Session = Depends(get_db)):
    data=AttendanceRepo.export_db(db)
    with open("exported_data.json", "w") as f:
        result=json.dump( (jsonable_encoder(data)),f)
    #     print(result)
    print(data)    
    
    return data
@router.get('/companies',tags=['Companies'])
async def get_companies(db: Session = Depends(get_db),current_user:AttendanceUser=Depends(get_current_user_from_bearer)): 
    now=datetime.now()
    print(now)
    companies_list=AttendanceRepo.companies_list(current_user,db) 
    
    # data={'companines':list(filter(lambda x:x.is_active==True  ,companies_list)),'inactive':list(filter(lambda x:x.is_active==False ,companies_list))}
    # print( datetime.now())
    return companies_list

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

@router.get('/profile',tags=['Employer Details'])
async def getProfile(current_user:AttendanceUser=Depends(get_current_user_from_bearer),db: Session = Depends(get_db)):
    return current_user


 
@router.get('/monthly-report',tags=[ 'Employer Report'])
async def getMonthlyReport(companyId,db:Session= Depends(get_db)):
    return AttendanceRepo.employeeWithAttendanceMonthlyReport(companyId,db)


@router.get("/weekly-report",tags=[ 'Employer Report'])
async def weeklyreport(companyId:int, db: Session = Depends(get_db)):
    dates= getWeekDate()
    weekdata=AttendanceRepo.employeewithAttendanceWeeklyReport(companyId,db)
    # weekdata=AttendanceRepo.getWeeklyAttendance(companyId,dates[0].date(),dates[1].date(), db)
 
    return weekdata
@router.get("/today-report",tags=[ 'Employer Report'])
async def attendance(companyId:int, db: Session = Depends(get_db),page:int=1,limit:int=10):
        return AttendanceRepo.employeeWithDailyReport(companyId,db,page-1,limit)
        # return AttendanceRepo.reportToday(companyId,db)

        # allAttendances=AttendanceRepo.todayReport(companyId,db)
        # return allAttendances
 


@router.get('/users',tags=['Companies'])#,response_model=list[AttendanceUser])
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

def update_employee_by_id(user:AttendanceUser,employee:Employee,employeeId:int,companyId:int,db):
    employee_update=db.get(EmployeeModel,employeeId)
    # Update the employee record with the new values from the dictionary
    for key, value in employee.dict().items():
        print(key)
        setattr(employee_update, key, value)
    # print(employee)
    db.commit()
    db.refresh(employee_update) 
    return employee_update 
@router.get('/get-employee-by-id',tags=['Companies'])
async def getEmployeeById(id:int,db: Session = Depends(get_db)):
    return db.get(EmployeeModel,id)
# def get_employee_by_id(user:AttendanceUser, employeeId:int,companyId:int,db):
@router.post("/register",tags=['Employer Register/Login'])#response_model = BaseAttendanceUser)
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

@router.post('/resend-otp',tags=['Employer Register/Login'])
async def resend_otp(phone:int,db: Session = Depends(get_db)):
    otp=create_otp(phone,db)
    return BaseAttendanceUser(phone=phone,otp=otp.code)

@router.post('/verify-otp',tags=['Employer Register/Login'])
def verify(otp:str=Body(...),phone:str=Body(...),db: Session = Depends(get_db),):
    return AttendanceRepo.verify_otp(otp,phone,db)
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

 
@router.post('/add-company',tags=['Companies'])#response_model=Company
def add_company(company:Company,db: Session = Depends(get_db),current_user:AttendanceUser=Depends(get_current_user_from_bearer)): 
    company=create_company(current_user,db,company)
    return company

@router.post('/get-companies',tags=['Companies'])
def all_companies(current_user:AttendanceUser=Depends(get_current_user_from_bearer),db: Session = Depends(get_db)):
    # print(current_user)
    company_list=AttendanceRepo.companies_list(user=current_user,db=db)
    
    return {"active":company_list}
posts=[]


@router.post('/add-employee',tags=['Companies'])
def add_employee(employee:Employee,companyId:int, current_user:AttendanceUser=Depends(get_current_user_from_bearer),db: Session = Depends(get_db)):
    employee=create_employee(current_user,db,employee,companyId)
    return employee  
@router.get('/employee-by-id')
async def getEmployee(employeeId:int, current_user:AttendanceUser=Depends(get_current_user_from_bearer),db: Session = Depends(get_db)):
    try:
        return db.get(EmployeeModel,id)
    except Exception as e:
        return HTTPException(status_code=404,detail='Employee not found')
@router.post('/update-employee',tags=['Companies'])
def update_employee(id:int,employee:Employee,companyId:int, current_user:AttendanceUser=Depends(get_current_user_from_bearer),db: Session = Depends(get_db)):
    employee=update_employee_by_id(current_user,employee,id,companyId,db)
    return employee  
@router.post('/add-approver',tags=['Companies'])
def add_approver(id:int,companyId:int, current_user:AttendanceUser=Depends(get_current_user_from_bearer),db: Session = Depends(get_db)):
    approver=AttendanceRepo.addApprover(id,companyId,db)
    return approver

@router.post("/send-invitation",tags=[ 'Companies'])
def sendInvitation(employeeId,current_user:AttendanceUser=Depends(get_current_user_from_bearer),db: Session = Depends(get_db)):
    employee=db.get(EmployeeModel,employeeId)
    employee.status=Status.INVITED
    db.commit()
    db.refresh(employee)
    return employee
    # invitation=AttendanceRepo.create_company_invitation(employeeId,companyId,db)
    # return invitation
def allemployees(id,db):
    return db.query(EmployeeModel).filter(EmployeeModel.company_id==id).all()
@router.get('/employee',tags=[ 'Companies'])
def all_employee(companyId:int,db: Session = Depends(get_db)):# current_user:AttendanceUser=Depends(get_current_user_from_bearer),
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