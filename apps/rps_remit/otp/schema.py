import datetime
import random
from typing import Optional
from sqlmodel import Field, SQLModel

from record_service.main import RecordService



class OTPSetupBase(SQLModel):
    id:str
    otp_code:str 
    phoneOrEmail:str 
    created_at:str 
    updated_at:str
    def setrand(self):
        self.code="{:04d}".format (random.randint(0, 9999))
        self.created_at=datetime.now()
    def isvalid(self):
        now:datetime=datetime.now()
        return (now-self.created_at)<datetime.timedelta(minutes=2)

    @property
    def is_valid(self):
        return True if (datetime.datetime.now()-self.created_at)<datetime.timedelta(minutes=3) else False
class OTPRead(OTPSetupBase):
    id:Optional[int] = Field(default=None, primary_key=True) 


class OTP(OTPSetupBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 


 
class OTPCreate(OTPSetupBase):
    pass

class HeroRead(OTPSetupBase):
    id:Optional[int] = Field(default=None, primary_key=True) 

class OTPUpdate(OTPSetupBase):
    pass

 