

from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from apps.rps_remit.gs_cloud_storage import generate_signed_url
from record_service.main import RecordService


class BannersBase(SQLModel):
 
    url:str=None
    image:str
    @property
    def image_url(self):
        return 'http://127.0.0.1:8000'+self.image
    @property 
    def get_image(self):
        return generate_signed_url(self.image)
    

class BannersCreate(BaseModel):
    url:str
    image:str
    

class BannersRead(BannersBase):
    id:Optional[int] = Field(default=None, primary_key=True) 

class BannersUpdate(BannersBase):
    pass

 
class Banners(BannersBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 
