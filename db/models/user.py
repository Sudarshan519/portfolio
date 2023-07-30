
from sqlalchemy import Column, Date, DateTime, Enum, Float,Integer, String,Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from db.base import Base
from pydantic import BaseModel

from schemas.attendance import RecivingMethod


class Documents(Base):
    id=Column(Integer,primary_key=True,index=True)
    type=Column(Enum(("PASSWORD","PASSWORD"),('DRIVING_LICENSE',"DRIVING_LICENSE"),("RESIDENT_CARD","RESIDENT_CARD",),("MY_NUMBER_CARD","MY_NUMBER_CARD")))
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

class Users(Base):
    id = Column(Integer,primary_key=True,index=True)
    # username = Column(String(60),unique=True,nullable=False)
    email = Column(String(60),nullable=False,unique=True,index=True)
    hashed_password = Column(String(256),nullable=False)
    is_active = Column(Boolean(),default=True)
    verified=Column(Boolean,default=True)
    kyc_verified=Column(Boolean,default=False)
    is_superuser = Column(Boolean(),default=False)
    is_staff=Column(Boolean,default=False)
    document=Column(Integer,ForeignKey(Documents.id))
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

    
class Banners(Base):
    id = Column(Integer,primary_key=True,index=True)
    url=Column(String,nullable=True)
    image=Column(String )
    @property
    def image_url(self):
        return 'http://127.0.0.1:8000'+self.image

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

class RemitLocations(Base):
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

    

class Transaction(Base):
    id=Column(Integer,primary_key=True,index=True)
    sender_id=Column(Integer,ForeignKey(Users.id))
    remarks=Column(String,nullable=True)
    from_location=Column(String,nullable=True)
    to_location=Column(String,nullable=True)
    receipt_id=Column(String,nullable=True)
    receipt=Column(String)
    charge=Column(Float)
    recipient_country=Column(String,nullable=True)
    amount=Column(String,nullable=True)
    created_at=Column(DateTime,default=func.now())
    updated_at=Column(DateTime,default=func.now(),onupdate=func.now())
    # receiver_id=Column()
