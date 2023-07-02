from db.models.attendance import  AttendanceUser, EmployeeModel,Otp,CompanyModel,EmployeeCompany,AttendanceModel,BreakModel
from requests import Session
from db.session import get_db
from schemas.attendance import Company,Employee
from fastapi import status,HTTPException
from fastapi import Depends, HTTPException, Request
from core.config import settings
from datetime import date, datetime, time, timedelta
from core.security import create_access_token
from schemas.attendance import Status
class AttendanceRepo:
    @staticmethod
    def get_employee(phone,db):
        employee=db.query(EmployeeModel).filter(EmployeeModel.phone==phone,EmployeeModel.company_id==companyId).first()
        if employee: 
            return
        else:
            raise HTTPException(status_code=404, detail="Hero not found")
    @staticmethod
    def get_today_details(employeeId,db,companyId):
        
            today_attendance=db.query(AttendanceModel).filter(AttendanceModel.employee_id==employeeId,AttendanceModel.company_id==companyId).first()#,AttendanceModel.attendance_date==datetime.now().date
            
            if not today_attendance:
                return AttendanceModel(attendance_date=datetime.now(),company_id=companyId,login_time=None,logout_time=None)
            else:
                return today_attendance
        
    @staticmethod 
    def updateInvitation(id,db):
        invitation=db.query(EmployeeCompany).filter(EmployeeCompany.id==id).first()

        if invitation:
            invitation.status=Status.ACCEPTED

            db.commit()
            db.refresh(invitation)
            return invitation
    @staticmethod
    def getInvitationByCompany(empId,db,accepted=False,active=True):
        invitations=db.query(EmployeeCompany).filter(EmployeeCompany.employee_id==empId,EmployeeCompany.is_accepted==accepted,EmployeeCompany.is_active==active).all()
        return invitations
    @staticmethod
    def create_company_invitation(empId,compId,db):
        invitation_exist=db.query(EmployeeCompany).filter(EmployeeCompany.employee_id==empId,EmployeeCompany.company_id==compId).first()
        if not invitation_exist:
            invitation=EmployeeCompany(employee_id=empId,company_id=compId)
            db.add(invitation)
            db.commit()
            db.refresh(invitation)
            return invitation
        else:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Invitation already exist.")
    @staticmethod 
    def verify_otp(code,phone,db):
        otp=db.query(Otp).filter(Otp.phone==phone).order_by(Otp.id.desc()).first()
        if otp is not None: 
        
            if otp.code==code:# and otp.isvalid():
                access_token=AttendanceRepo.create_token(phone,db)
               
                return access_token
            else:
                return HTTPException(status_code=401,detail=f"Otp does not match.")
        else:
            return HTTPException(status_code=404,detail=f"Otp not found for user {phone}")
    @staticmethod
    def get_employee(phone:str,db):
 
        employee=db.query(EmployeeModel).filter(EmployeeModel.phone== phone).first()
 
        if employee is not None:
            return employee
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee does not exist.")
    @staticmethod
    def create_token(phone,db):
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(phone)}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "Bearer"}
    @staticmethod
    def create_otp(phone,db):
        otp=Otp(phone=phone)
        otp.setrand()
        db.add(otp)
        db.commit()
        db.refresh(otp)
        return otp

    @staticmethod
    def create_user(phone,db,is_employer:bool=False):
        try:
            user=AttendanceUser(phone=phone,is_employer=is_employer)
            db.add(user)
            db.commit() 
            db.refresh(user)
            return user
        except Exception as e:
            return HTTPException(status_code=400,detail=f'{e}')
        
    @staticmethod
    def get_user(phone,db):
        user=db.query(AttendanceUser).filter(AttendanceUser.phone==phone).first()
        if not user:
            # return HTTPException(status_code=404,detail="User does not exist.")
            return None
        return user
    @staticmethod
    def update_user(id:int,db,userupdate):
        try:
            user=db.get(AttendanceUser,id)
            print(userupdate)
            if not user:
                raise HTTPException(status_code=404, detail="Hero not found")
            for key, value in userupdate.items():
                setattr(user, key, value)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except:
            print
    @staticmethod
    def create_company(user:AttendanceUser,db:Session,company:Company):
        try:
            # name=company.name,address=company.address,start_time=company.start_time,end_time=company.end_time,established_date=company.established_date
            new_company=CompanyModel(**company.dict(), user_id=user.id,is_active=True)
            db.add(new_company)
            db.commit()
            db.refresh(new_company)
    
            return new_company
        except Exception as e:
            return HTTPException(status_code=status.HTTP_409_CONFLICT,detail=e)

    @staticmethod
    def companies_list(user:AttendanceUser,db:Session):

        try: 
            companies= db.query(CompanyModel).filter(CompanyModel.user_id==user.id).all()  
            return companies
        except Exception as e:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=e)
    @staticmethod
    def create_employee(user:AttendanceUser,db:Session,employee:Employee,companyId:int):
        try:
            
            new_employee=EmployeeModel(**employee.dict(), user_id=user.id,company_id=companyId)
            db.add(new_employee)
            db.commit()
            db.refresh(new_employee) 
            return new_employee

        except Exception as e:
            return HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Employee is already registered.")
