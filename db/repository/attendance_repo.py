import math
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
from sqlalchemy import and_, desc, func
from sqlalchemy import or_, and_
from week_util import getMonthRange, getWeekDate
from sqlalchemy.orm import joinedload,declarative_base
from db.models.attendance import Base
import json
# Base = declarative_base()
# 9863450107
# 0689
class AttendanceRepo:
    @staticmethod
    def employee_companies(phone,db):
        all=db.query(Employee).filter(EmployeeModel.phone==phone).all()
                # all=db.query(EmployeeModel,CompanyModel).filter(EmployeeModel.phone==phone).distinct(EmployeeModel.id).all()
                # companies=[]
                # for company,employee in all:
                #     if employee in companies:
                #         pass
                #     else:  
                #         # compdict=company.dict()
                #         # compdict['status']=employee.status
                #         companies.append(employee)
                
        return all
    @staticmethod
    def add_approver(empId,companyId,db):
        employee =db.get(EmployeeModel,empId)
        employee.is_approver=True
        db.commit()
        return db.refresh(employee)
        
    @staticmethod
    def serialize_instance(obj):
        return obj.to_dict()
    @staticmethod
    def import_db_from_json(data_dict,db):
        modelslist = Base.__subclasses__()
        
        data = {}
        for model in modelslist:
            db.query(model) .delete()
            db.bulk_insert_mappings(
            model,data_dict[model.__name__])

            db.commit()
            # if model.__name__=='Otp':
                # otps=[Otp() for otp in data_dict[model.__name__]]
                # print(otps)
                # db.bulk_save_objects(otps)
            
                # print([Otp(**data) in data for data_dict[model.__name__]])
    @staticmethod
    def export_db(db): 
        modelslist = Base.__subclasses__()
        print(modelslist)
        data = {}

        for model in modelslist:
            model_data = db.query(model).all()
            data[model.__name__] = [item.__dict__  for item in model_data]
        

        return data
        # data = db.query(Base).all()
        # json_data = [item.to_dict() for item in data]

        # with open("exported_data.json", "w") as f:
        #     json.dump(json_data, f, indent=4)
        # return json_data
    @staticmethod
    def updateEmployee(id,employee,db,compId):
        return db.query(AttendanceModel).filter(AttendanceModel.company_id==companyId).all()
    @staticmethod
    def getAllAttendance(companyId,db):
        return db.query(AttendanceModel).filter(AttendanceModel.company_id==companyId).all()
    @staticmethod
    def getWeeklyAttendance(companyId,startDate,endDate,db):
        return db.query(AttendanceModel).filter(AttendanceModel.company_id==companyId,AttendanceModel.attendance_date.between(startDate,endDate)).all()
    @staticmethod
    def store_break_start(attendanceId:int,db):
        new_break=BreakModel(attendance_id=attendanceId,break_start=datetime.now().time())
        db.add(new_break)
        db.commit()
        db.refresh(new_break)
        return new_break
    @staticmethod 
    def store_break_stop(breakId:int,db):
        break_to_update=db.get(BreakModel,breakId)
        break_to_update.break_end=datetime.now().time()
        db.commit()
        db.refresh(break_to_update)
        return break_to_update
    @staticmethod
    def get_all_attendance(compId,empId,db,):
        attendancelist=db.query(AttendanceModel).filter(AttendanceModel.employee_id==empId,AttendanceModel.company_id==compId,AttendanceModel.attendance_date==datetime.today().date()).order_by(AttendanceModel.id).all()#.desc(),AttendanceModel.attendance_date==datetime.now().date
    
        return attendancelist
    
    @staticmethod
    def store_logout(attendanceId,logoutTime,db):
        attetndance=db.get(AttendanceModel,attendanceId)
        print(logoutTime)
        attetndance.logout_time=logoutTime
        db.commit()
        db.refresh(attetndance)
        return attetndance
    @staticmethod
    def store_attendance(compId,empId,db,loginTime,logoutTime):
        attendance=AttendanceModel(attendance_date=datetime.today(), company_id=compId,employee_id=empId,login_time=loginTime,logout_time=logoutTime)
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        return attendance
    @staticmethod
    def get_employee(phone,db,companyId):
        employee=db.query(EmployeeModel).filter(EmployeeModel.phone==phone,EmployeeModel.company_id==companyId).first()
        if employee: 
            return
        else:
            raise HTTPException(status_code=404, detail="Hero not found")
    @staticmethod
    def get_today_details(employeeId,db,companyId):
        
            today_attendance= attendancelist=db.query(AttendanceModel).filter(AttendanceModel.employee_id==employeeId,AttendanceModel.company_id==companyId,AttendanceModel.attendance_date==datetime.today() ).order_by(AttendanceModel.id).first()#.desc(),AttendanceModel.attendance_date==datetime.now().date
            
            if not today_attendance:
                return AttendanceModel(id=-1, attendance_date=datetime.now(),company_id=companyId,employee_id=employeeId,login_time=None,logout_time=None)
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
        print(otp.code)
        if otp is not None: 
            if otp.code==code:# and otp.isvalid():
                access_token=AttendanceRepo.create_token(phone,db)
                access_token['companies']= []
                
                return access_token
            else:
                return HTTPException(status_code=401,detail=f"Otp does not match.")
        else:
            return HTTPException(status_code=404,detail=f"Otp not found for user {phone}")
    @staticmethod
    def get_employee(phone:str,db,companyId):
 
        employee=db.query(EmployeeModel).filter(EmployeeModel.phone== phone,EmployeeModel.company_id==companyId).first()
 
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
        data=[]
         
        try: 
            companies= db.query(CompanyModel).filter(CompanyModel.user_id==user.id).all() 
            # for company in companies :
            #     data={
            #         "id":company.id,
            #         "name":company.name,
            #         "start_time":company.start_time,
            #         "employee":company.employee
            #     }
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
    @staticmethod
    def allemployees(id,db):
        return db.query(EmployeeModel).filter(EmployeeModel.company_id==id).all()
    
    @staticmethod
    def employeeWithDailyReport(companyId,db):
        now=datetime.now()
        employees = db.query(EmployeeModel, AttendanceModel).outerjoin(AttendanceModel).filter( or_(
            AttendanceModel.attendance_date == date.today(),
            AttendanceModel.attendance_date.is_(None)
        )) .order_by( (AttendanceModel.attendance_date)).all()#  | AttendanceModel.attendance_date.is_(None)
        attendance_data = {}
        result=[]
        # candidates = db.query(EmployeeModel,AttendanceModel).join(AttendanceModel).filter(AttendanceModel.attendance_date==datetime.now().today().date()).all()#
        for employee,attendance in employees:
            employee_id = employee.id
            if employee_id not in attendance_data:
                attendance_data[employee_id] = {
                    "employee": employee.phone,
                    "company_id":employee.company_id,
                    "attendance": []
                }
            # print(attendance)
            if attendance:
                attendance_data[employee_id]["attendance"].append( 
                    attendance  
                # "attendance_id": attendance.id,
                # "date": attendance.attendance_date,
                # "status": attendance.status
                ) 
        for k,v in attendance_data.items():
            result.append(v)      
        print(datetime.now()-now)
        return  result
    @staticmethod
    def employeewithAttendanceWeeklyReport(companyId,db,):
        dates= getWeekDate()
        now=datetime.now()
        # dates= getMonthRange(2023,6)
        data=[]
        print(dates[0])
        print(dates[1])
        # candidates=( db.query(EmployeeModel) 
        #                 #  .outerjoin(AttendanceModel, 
        #                 #            and_(  AttendanceModel.attendance_date.between(dates[0],dates[1]))# == date.today())
        #                 #             ) 
        #                 #  .filter(EmployeeModel.company_id==companyId)
        #                  .all() )
        # candidates = db.query(EmployeeModel).filter(EmployeeModel.attendance.any(AttendanceModel.attendance_date.between(dates[0].date(),dates[1].date()))).all()
        # for candidate in candidates:
           
        #     attendance_records = [
        #         {
        #             "date": attendance.attendance_date,
        #             "login_ time":attendance.login_time,
        #             "logout_time":attendance.logout_time,
        #             "breaks":attendance.breaks,
        #             "hours_worked":attendance.hours_worked
        #             # "status": attendance.status
        #         }
        #         for attendance in candidate.attendance
        #         if attendance.attendance_date >= dates[0].date()
        #     ]
        #     data.append({
        #         "id": candidate.id,
        #         "name": candidate.name,
        #         # "email": candidate.email,
        #         "attendance": attendance_records
        #     })
        
        # Retrieve all employees with attendances within the date range
        employees = db.query(EmployeeModel, AttendanceModel).outerjoin(AttendanceModel).filter(AttendanceModel.attendance_date.between(dates[0], dates[1]) | AttendanceModel.attendance_date.is_(None)).all()#.filter(AttendanceModel.attendance_date.between(dates[0], dates[1]) | AttendanceModel.attendance_date.is_(None)).all()
        # Process the results
        attendance_data = {}
        result=[]
        # candidates = db.query(EmployeeModel,AttendanceModel).join(AttendanceModel).filter(AttendanceModel.attendance_date==datetime.now().today().date()).all()#
        for employee,attendance in employees:
            employee_id = employee.id
            if employee_id not in attendance_data:
                attendance_data[employee_id] = {
                    "employee": employee.phone,
                    "attendance": []
                }
            # print(attendance)
            if attendance:
                attendance_data[employee_id]["attendance"].append( 
                    attendance  
                # "attendance_id": attendance.id,
                # "date": attendance.attendance_date,
                # "status": attendance.status
                ) 
        for k,v in attendance_data.items():
            result.append(v)      
        print(datetime.now()-now)
        return  result#attendance_data#[attendance_data
            #]
            # print(f"Employee ID: {employee.id}, Name: {employee.name}")
        #     if attendance:
        #         emp_dict['attendance_date']=attendance.attendance_date
        #         emp_dict['attendance_time']=attendance.login_time
        #         emp_dict['clock_out_time']=attendance.logout_time
        #         emp_dict['hour_worked']=attendance.hours_worked
        #         # print(f"Attendance ID: {attendance.id}, Date: {attendance.attendance_date}, LOGIN:{attendance.login_time}, LOGOUT:{attendance.login_time}")
        #         data.append(emp_dict)
        #     else:
        #         data.append(emp_dict)
        #         # print(f"Attendance ID: NIL")
        # return attendance_data
    
    @staticmethod
    def employeeWithAttendanceMonthlyReport(companyId,db):
        now=datetime.now()
        # print(now)
        dates= getMonthRange(now.year,now.month)
        # print(dates)
        employees=db.query(EmployeeModel,AttendanceModel).outerjoin(AttendanceModel).filter(AttendanceModel.attendance_date.between(dates[0], dates[1]) | AttendanceModel.attendance_date.is_(None),AttendanceModel.company_id==companyId).order_by((AttendanceModel.attendance_date)).all()
        attendance_data = {}
        employee_count=db.query(EmployeeModel).filter(EmployeeModel.company_id==companyId).count()
        present_count=0
        absent_count=0
        result=[]
        for employee,attendance in employees:
                employee_id = employee.id
                if employee_id not in attendance_data:
                    attendance_data[employee_id] = {
                        "employee": employee.phone,
                        "company_id":employee.company_id,
                        "attendance": []
                    }

                # print(attendance)
                
                if attendance:
                    present_count+=1
                    attendance.breaks
                    attendance_data[employee_id]["attendance"].append( 
                  attendance,
                  
                    # "attendance_id": attendance.id,
                    # "date": attendance.attendance_date,
                    # "status": attendance.status
                    )
                else:
                    absent_count+=1
                # print(attendance_data[employee_id]["attendance"])
                attendance_data[employee_id]["present_count"]=len(attendance_data[employee_id]["attendance"])
        for k,v in attendance_data.items():
            result.append(v)
        # print(result)

                    # print(len(attendance_data[employee_id]["attendance"]))
                
        # print(datetime.now())
        # print(now)
        print(datetime.now()-now)
        # print(present_count)
        # print(absent_count)
        # print(employee_count)
        # attendance_data['present_count']=present_count
        # attendance_data['absent_count']=employee_count*30-present_count
        return result
        # data=[
        #     {
        #         'employee':employee,
        #         'attendance':attendance
        #     }
        #     for employee,attendance 
        #     in employees 
        #     # if attendance.attendance_date>(dates[0])
        #     # and attendance.attendance_date<(dates[1])
        # ]
        # for employee,attendance in employees:
            
        #     # print(employee)
        #     data.append({
        #         'employee':employee,
        #         'attendance':attendance
        #     })
        # return data
        # data=[]
        # attendance_data = {}
        # employees = ( db.query(EmployeeModel) 
        #                  .outerjoin(AttendanceModel, 
        #                            and_(  AttendanceModel.attendance_date.between(dates[0],dates[1]))# == date.today())
        #                             ) 
        #                  .filter(EmployeeModel.company_id==companyId)
        #                  .all() )
        
        # # print(db.query(EmployeeModel,AttendanceModel).join(AttendanceModel).filter(AttendanceModel.attendance_date.between(dates[0],dates[1])).count())#)
        # # candidates = db.query(EmployeeModel,AttendanceModel).join(AttendanceModel).filter(AttendanceModel.attendance_date.between(dates[0],dates[1])).all()#
        # for employee ,attendance in employees: 
        #     count=0
        #     for attendance in employee.attendance:
        #         count=count+attendance.hours_worked
        #     print(count)
        #     # if employee_id not in attendance_data:
        #     attendance_records = [
        #         {
                    
        #             "date": attendance.attendance_date,
        #             "login_time":attendance.login_time,
        #             "logout_time":attendance.logout_time,
        #             "breaks":attendance.breaks,
        #             "hours_worked":attendance.hours_worked
        #             # "status": attendance.status
        #         }
        #         for attendance in employee.attendance]
        #     data.append({ "present":len(employee.attendance,),#np.unique(dates.date) for unique date
        #         "id": employee.id,
        #         "name": employee.name,
        #         "present":count,
        #         # "company":employee.company,
        #         # "email": candidate.email,
        #         "attendance": attendance_records
        #     })
        
        # return  data 
        # candidates = db.query(EmployeeModel).join(AttendanceModel).filter(AttendanceModel.attendance_date.between(dates[0],dates[1])).all()
        # for candidate in candidates:
           
        #     attendance_records = [
        #         {
        #             "date": attendance.attendance_date,
        #             "login_time":attendance.login_time,
        #             "logout_time":attendance.logout_time,
        #             "breaks":attendance.breaks,
        #             "hours_worked":attendance.hours_worked
        #             # "status": attendance.status
        #         }
        #         for attendance in candidate.attendance
        #     ]
        #     data.append({ "present":len(candidate.attendance,),#np.unique(dates.date) for unique date
        #         "id": candidate.id,
        #         "name": candidate.name,
        #         # "email": candidate.email,
        #         "attendance": attendance_records
        #     })
        # return data
    @staticmethod
    def employeewithAttendance(companyId,db):
        data=[]
        # today=datetime.today().strftime("%Y-%m-%d")
        # print(today)
        candidates = db.query(EmployeeModel).join(AttendanceModel)
        candidates=candidates.filter(AttendanceModel.attendance_date==datetime.today().date(),AttendanceModel.company_id==companyId,)
        results=candidates.all()
        for candidate in results:
            
            attendance_records = [
                {
                    "date": attendance.attendance_date,
                    "login_time":attendance.login_time,
                    "logout_time":attendance.logout_time,
                    "breaks":attendance.breaks,
                    "hours_worked":attendance.hours_worked
                    # "status": attendance.status
                }
                for attendance in candidate.attendance
            ]
            data.append({ "present":len(candidate.attendance,),#np.unique(dates.date) for unique date
                "id": candidate.id,
                "name": candidate.name,
                # "email": candidate.email,
                "attendance": attendance_records
            })
        return data
    @staticmethod
    def newtodayReport(companyId,db):
        query=db.query(EmployeeModel)

    
    @staticmethod
    def todayReport(companyId,db,page=1,limit=100):
        data=[]
        attendance_data = {}
        offset_page = page - 1
        try:
            employees =  db.query(EmployeeModel).offset(offset_page*limit).limit(limit) .all()
                        #  .outerjoin(AttendanceModel, 
                        #         #    and_(AttendanceModel.attendance_date == date.today()
                        #         #         ,AttendanceModel.company_id==companyId)
                        #             )  
        
            
            employees_count=db.query(EmployeeModel).count()
            total_page = math.ceil(employees_count / limit)
 
            attendance_count=db.query(AttendanceModel).filter(AttendanceModel.attendance_date == date.today(),AttendanceModel.company_id==companyId).count()
 
            employee_data = []
 
            for employee in employees:
                # print(employee)
                records=[
                    attendance 
                    for attendance in employee.attendance
                    if attendance.attendance_date ==date.today()
                ]  
                employee_data.append({
                    'name':employee.name,
                        
                    'today_attendance':records[0] if records else None})
               
                
            
            return {"present_count":attendance_count,"absent_count":employees_count-attendance_count,"employees_all":employee_data,"currentPage":page,"nextPage":page+1,"total_page":total_page}
        except Exception as e:
            return e
    
    @staticmethod
    def reportToday(companyId,db):
        now=datetime.now()
        # Retrieve all employees from the database
        employees = db.query(EmployeeModel).filter(EmployeeModel.company_id==companyId ).all()#.distinct(EmployeeModel.id)
        data=[]
        present_count=0
        # Retrieve attendance records for today
        today = date.today()
        for employee in employees:
            dict=({
                    'id':employee.id,
                    'name':employee.name,
                    'phone':employee.phone,
                    'company_id':employee.company_id,
                    
                   })
            attendances_today = [attendance for attendance in employee.attendance if attendance.attendance_date == today]
 
            if attendances_today:

                present_count+=1
                for attendance in attendances_today:
                    dict['attendance']=attendance 
            else:
                dict['attendance']=None
            data.append(dict)
            total=len(data)

        print(datetime.now())
        print(now)
        print(datetime.now()-now)
        return {
            'total':total,
            'present_count':present_count,
            
            'absent_count':total-present_count,
            'data':data}