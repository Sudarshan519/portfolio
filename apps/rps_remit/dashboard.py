from ast import List
from fastapi import APIRouter, Body,Depends, File, Form, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from apps.rps_remit.fireabse_bucket import upload_file
from apps.rps_remit.gs_cloud_storage import upload_to_gcs

from db.models.user import Banners, Users
from db.session import get_db
from other_apps.upload_file import firebase_upload


router=APIRouter(tags=['Dashboard'])

@router.get("/")
def index():
   return {"message": "Hello World from remit dashboard app"}
class UserSchema(BaseModel):
   id:int
   email:str
   verified:bool
   is_active:bool

   class Config:
      orm_mode=True

@router.post('/login')
async def login(username:str,password:str):
   pass
@router.get('/users',response_model=list[UserSchema])
def all_users(db:Session=Depends(get_db)):
   return db.query(Users).filter(Users.is_superuser==False).all()
class BannerSchema(BaseModel):
   url:str
   image:str 
   class Config:
      orm_mode=True

@router.post("/banners")
async def add_banner(url:str=Body( ),image:UploadFile =File(...),db:Session=Depends(get_db)):
   file_content=await image.read()
   filename=image.filename
   upload_to_gcs(filename,file_content ,image.content_type)
   if image:
      
      with open("images/"+filename, 'wb') as f:
            while contents := image.file.read(1024 * 1024):
                    f.write(contents)
      image_url='/images/'+filename
      # await upload_file(image)
      # print(image.filename)
      # ext= image.filename.split(".")[-1]
      # image_url=firebase_upload(image.file.read(),ext,image.filename)
      # print(image_url)
   banner=Banners(url=url,image=image_url)
   db.add(banner)
   db.commit()
   db.refresh(banner)
   return banner
