
from datetime import timedelta
import datetime
from sqlalchemy import Column, Date, DateTime, Enum, Float,Integer, String,Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from apps.rps_remit.gs_cloud_storage import generate_signed_url
from db.base import Base
from pydantic import BaseModel

from schemas.attendance import RecivingMethod, UserKycStatus

class ForeignExchangeCharge(Base):
    id=Column(Integer,primary_key=True,index=True)
    min_amount=Column(Float,default=1000)
    # charge_upto_one_lakh_in_rs=Column(Float,default=250)
    charge_upto_one_lakh_in_percentage=Column(Float,default=2) 
    charge_from_one_ten_lakh_in_percentage=Column(Float,default=1)
    charge_from_one_ten_lakh_in_percentage=Column(Float,default=.5)
    created_at=Column(DateTime,default=func.now())
    updated_at=Column(DateTime,default=func.now(),onupdate=func.now())
    cancellation_charge=Column(Float,default=250) 
    issuance_charge=Column(Float,default=500)


class Documents(Base):
    id=Column(Integer,primary_key=True,index=True)
    type=Column(Enum(("PASSPORT","PASSPORT"),('DRIVING_LICENSE',"DRIVING_LICENSE"),("RESIDENT_CARD","RESIDENT_CARD",),("MY_NUMBER_CARD","MY_NUMBER_CARD")))
    passport_img=Column(String,nullable=True)
    driving_license=Column(String,nullable=True)
    my_number_card=Column(String,nullable=True)
    residence_card=Column(String,nullable=True)



# class UserType(str,Enum):
#     pass
class TransactionPin(Base):
    id=Column(Integer,primary_key=True,index=True)
    tpin=Column(Integer)
    expiry_date=Column(Date)



class KycType(Base):
    # limit on transaction
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False,default='')
    total_limit=Column(Integer,default=0)
    per_day_limit=Column(Integer,default=0)
    per_month_limit=Column(Integer,default=0)
    per_year_limit=Column(Integer,default=0)

    # limit on amount
    per_day_amount=Column(Integer,default=0)
    per_month_amount=Column(Integer,default=0)
    per_year_amount=Column(Integer,default=0)

class Users(Base):
    id = Column(Integer,primary_key=True,index=True)
    # username = Column(String(60),unique=True,nullable=False)
    email = Column(String(60),nullable=False,unique=True,index=True)
    phone=Column(String(16),nullable=True)
    photo=Column(String(256),nullable=True)
    phone_verified=Column(Boolean,default=False)
    hashed_password = Column(String(256),nullable=False)
    is_active = Column(Boolean(),default=True)
    verified=Column(Boolean,default=False)
    kyc_status=Column(Enum(UserKycStatus),default=UserKycStatus.UNVERIFIED)
    kyc_verified=Column(Boolean,default=False)
    # full_kyc=Column(Boolean,default=False)
    is_superuser = Column(Boolean(),default=False)
    is_staff=Column(Boolean,default=False)
    role=Column(String,default='')
    document=Column(Integer,ForeignKey(Documents.id),nullable=True)
    kycType=Column(Integer,ForeignKey(KycType.id),nullable=True)
    # limit on transaction
    total_limit=Column(Integer,default=0)
    per_day_limit=Column(Integer,default=0)
    per_month_limit=Column(Integer,default=0)
    per_year_limit=Column(Integer,default=0)
    # limit on amount
    per_day_amount=Column(Integer,default=0)
    per_month_amount=Column(Integer,default=0)
    per_year_amount=Column(Integer,default=0)

    @property
    def check_transaction_limit(self,db):
        return True
    @property
    def email_verified(self):
        return self.verified

class Banners(Base):
    id = Column(Integer,primary_key=True,index=True)
    url=Column(String,nullable=True)
    image=Column(String )
    @property
    def image_url(self):
        return 'http://127.0.0.1:8000'+self.image
    @property 
    def get_image(self):
        return generate_signed_url(self.image)

class OTPSetup(Base):
    id=Column(Integer,primary_key=True,index=True)
    otp_code=Column(Integer,nullable=False)
    userid=Column(Integer,ForeignKey(Users.id),nullable=False)
    created_at=Column(DateTime,default= func.now())
    updated_at=Column(DateTime,default=func.now(),onupdate=func.now())
    @property
    def is_valid(self):
        return True if (datetime.datetime.now()-self.created_at)<timedelta(minutes=2) else False

class ExchangeRate(Base):
    id=Column(Integer,primary_key=True,index=True)
    published_on=Column(DateTime,nullable=True)
    modified_on=Column(DateTime,nullable=True)
    date=Column(Date,primary_key=False)
    rates=relationship("Rates")#,back_populates="exchangerate")

class Rates(Base):
    id=Column(Integer,primary_key=True,index=True)
    iso3=Column(String,nullable=True)
    name=Column(String,nullable=True)
    unit=Column(Integer,nullable=True)
    buy=Column(String,nullable=True)
    sell=Column(String,nullable=True)
    rate=Column(Integer,ForeignKey(ExchangeRate.id),nullable=False)
    # exchangerate=relationship("Rates",)#back_populates="rates")




class RecivingMethods(Base):
    id=Column(Integer,primary_key=True,index=True)
    status=Column(Enum(RecivingMethod),default=RecivingMethod.CASH)
    name=Column(String,nullable=False)
    address=Column(String,nullable=True)
    idorNumber=Column(String,nullable=True)
    logo=Column(String,nullable=True)


class Benificary(Base):
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,)
    phone=Column(String)
    address=Column(String)
    relationship=Column(String)

class RemitLocations(Base):
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    address=Column(String,nullable=False)
    phone=Column(String,nullable=False)
    latlng=Column(String,nullable=False)
    country=Column(String,nullable=False)

class BankDepositLocations(Base):
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    address=Column(String,nullable=False)
    phone=Column(String,nullable=False)
    latlng=Column(String,nullable=False)
    country=Column(String,nullable=False)
     
class Receipt(Base):
    id=Column(Integer,primary_key=True,index=True)
    amount=Column(Float)
    used=Column(Boolean,default=False)
    country=Column(Boolean,nullable=True)

# class TransactionState(Base):
#     pass

class Transaction(Base):
    id=Column(Integer,primary_key=True,index=True)
    sender_id=Column(Integer,ForeignKey(Users.id),nullable=True)
    remarks=Column(String,nullable=True)
    from_location=Column(String,nullable=True)
    to_location=Column(String,nullable=True)
    receipt_id=Column(String,nullable=True)
    receipt=Column(String,)
    charge=Column(Float,)
    recipient_country=Column(String,nullable=True)
    amount=Column(String,nullable=True)
    created_at=Column(DateTime,default=func.now())
    updated_at=Column(DateTime,default=func.now(),onupdate=func.now())
    paymentMode=Column(String,primary_key=True )



    # receiver_id=Column()
class Receiver(Base):
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,primary_key=True)
    gender=Column(String,primary_key=True)
    mobile=Column(String,primary_key=True)
    relationship=Column(String,primary_key=True)
    address=Column(String,primary_key=True)
    
    bankBranchId=Column(String)
    accountNumber=Column(String) 
    otp=Column(String)

class Permissions(Base):
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False,unique=True)
    # role=Column(Integer,ForeignKey("Role.id"),)
    # roles=relationship("Role",back_populates="permission")
# class UserPermissons(Base):
#     id=Column(Integer,primary_key=True,index=True)
#     name=Column(String,nullable=False,unique=True)
#     role_id=Column(Integer,ForeignKey("Role.id"),nullable=True )
#     roles=relationship("Role",back_populates="permission")
# class Role(Base):
#     id=Column(Integer,primary_key=True,index=True)
#     name=Column(String,nullable=False,unique=True)
#     permissions=relationship("UserPermissons",back_populates="role")

def all_permissons():

    permissionlist=['add','update','delete','view']
    modelslist = Base.__subclasses__()
    models=[]
    for model in modelslist:
        for permision in permissionlist:
            models.append(model.__name__+":"+permision)
            
    return models

