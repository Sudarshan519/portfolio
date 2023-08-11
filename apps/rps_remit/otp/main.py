from fastapi import APIRouter, Depends
from apps.rps_remit.otp.schema import OTP
from sqlmodel import Session
from apps.rps_remit.user.schema import RemitUser

from db.session_sqlmodel import get_session
app=APIRouter(prefix='/otp',tags=['OTP'])


class OTPService:
    @staticmethod
    def verify_otp(email,code,db:Session):
        otp=db.query(OTP).where(OTP.phoneOrEmail==email).order_by(OTP.id.desc()).first()
        if code==otp.otp_code:
                return True
        return False
    @staticmethod
    def create_otp(phoneOrEmail,db):
        otp=OTP(phoneOrEmail=phoneOrEmail)
        otp.setrand()
        db.add(otp)
        db.commit()
        db.refresh(otp)
        return otp


class MessageService:
     @staticmethod
     async def send_message(message:str,phone:str):
          return {}



@app.post('/setup-phone')
async def phone_setup(phone,db:Session=Depends(get_session)):
    user=db.query(RemitUser).where(RemitUser.phone==phone,RemitUser.phone_verified==True).first()
    if user:
        return {"status":"failed","data":"Mobile Number already registered"}

    otp=OTPService.create_otp(phone,db)
    return {"status":"success","data":"OTP Sent to your mobile."}


@app.post('/verify-phone')
async def verify_phone(phone,code,db:Session=Depends(get_session)):
    user=db.query(RemitUser).where(RemitUser.phone==phone,RemitUser.phone_verified==True).first()
    if user:
        return {"status":"failed","data":"Mobile Number already registered"}

    otp_verified=OTPService.verify_otp(phone,code,db)
    if otp_verified:
         
        return {"status":"success","data":"OTP verified successfully."}
    return {"status":"failed","data":"Invalid otp"}


@app.post('/verify-email')
async def verify_email(email,code,db:Session=Depends(get_session)):
    user=db.query(RemitUser).where(RemitUser.email==email).first()
 
    if not user:
        
        
 
        return {"status":False,"data":"Email verified failed"}

    otp_verified=OTPService.verify_otp(email,code,db)
    if otp_verified:
        user.verified = True
        db.commit()
        db.refresh(user)
 
        
         
        return {"status":"success","data":"Email verified successfully."}
    return {"status":"failed","data":"Invalid otp"}

