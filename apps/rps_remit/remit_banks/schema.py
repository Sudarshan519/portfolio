from typing import Optional
from sqlmodel import Field, SQLModel

from record_service.main import RecordService


class JapanBankBase(SQLModel):
    name:str
    account_number:str
    contact:str
    address:str
    currency:str
    total_balance:float
class JapanBank(JapanBankBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 


class JapanBankRead(JapanBankBase):
    id:Optional[int] = Field(default=None, primary_key=True) 
    # recivingmethod: List[RecivingMethod]


class JapanBankCreate(JapanBankBase):
    pass
 
class JapanBankUpdate(JapanBankBase):
    pass

class NepalBankBase(SQLModel):
    name:str
    account_number:str
    contact:str
    address:str
    currency:str
    total_balance:float
class NepalBank(NepalBankBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 
class NepalBankRead(NepalBankBase):
    id:Optional[int] = Field(default=None, primary_key=True) 
    # recivingmethod: List[RecivingMethod]


class NepalBankCreate(NepalBankBase):
    pass
 
class NepalBankUpdate(NepalBankBase):
    pass
