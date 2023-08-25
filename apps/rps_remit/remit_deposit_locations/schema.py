from sqlmodel import SQLModel


class RemitDepostBase(SQLModel):
    name:str
    location:str
    phone:str
    mobile:str
    logo:str
    country:str
    

from typing import Optional
from sqlmodel import Field, SQLModel

from record_service.main import RecordService

 

class RemitDepost(RemitDepostBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 


class RemitDepostRead(RemitDepostBase):
    id:Optional[int] = Field(default=None, primary_key=True) 
    # recivingmethod: List[RecivingMethod]


class RemitDepostCreate(RemitDepostBase):
    pass
    class Config:
        schema_extra={
            "example":{
            "name": "Rps Remit",
           
            "mobile":"0809090909099",
            "phone": 9800000000,
            "logo":"",
            "country":"Japan",
            "location":"Tokyo"
            }
        }
 
class RemitDepostUpdate(RemitDepostBase):
    pass

