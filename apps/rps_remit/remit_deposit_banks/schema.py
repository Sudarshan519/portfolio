from typing import Optional
from sqlmodel import Field, SQLModel

from record_service.main import RecordService


class RemitBankDepositBase(SQLModel):
    bank_name:str
    logo:str
    account_holder_name:str
    account_number:str
    phone:str



class RemitBankDeposit(RemitBankDepositBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 


class RemitBankDepositRead(RemitBankDepositBase):
    id:Optional[int] = Field(default=None, primary_key=True) 
    # recivingmethod: List[RecivingMethod]


class RemitBankDepositCreate(RemitBankDepositBase):
    pass
    class Config:
        schema_extra={
            "example":{
            "bank_name": "NMB",
            "logo": "",
            "account_holder_name": "RPS",
            "account_number":"0809090909099",
            "phone": 9800000000,
            
            }
        }
 
class RemitBankDepositUpdate(RemitBankDepositBase):
    pass

