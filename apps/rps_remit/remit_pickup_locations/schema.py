from typing import Optional
from sqlmodel import Field, SQLModel

from record_service.main import RecordService


class CashPickUpBase(SQLModel):
    name:str
    address:str
    phone:str


class CashPickup(CashPickUpBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 


class CashPickupRead(CashPickUpBase):
    id:Optional[int] = Field(default=None, primary_key=True) 
    # recivingmethod: List[RecivingMethod]


class CashPickupCreate(CashPickUpBase):
    pass
    class Config:
        schema_extra={
            "example":{
            "name": "Rps Remit",
           
            "address":"0809090909099",
            "phone": 9800000000,
            
            }
        }
 
class CashPickupUpdate(CashPickUpBase):
    pass

