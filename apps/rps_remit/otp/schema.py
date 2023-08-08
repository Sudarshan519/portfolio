import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

from record_service.main import RecordService



class OTPSetupBase(SQLModel):
    id:str
    otp_code:str 
    userid:str 
    created_at:str 
    updated_at:str
    @property
    def is_valid(self):
        return True if (datetime.datetime.now()-self.created_at)<datetime.timedelta(minutes=3) else False
class OTPRead(OTPSetupBase):
    id:Optional[int] = Field(default=None, primary_key=True) 


class OTP(OTPSetupBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 
