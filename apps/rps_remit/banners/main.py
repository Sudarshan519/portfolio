from fastapi import APIRouter, Body, Depends, File, UploadFile
from requests import Session
from apps.rps_remit.gs_cloud_storage import upload_to_gcs
from db.session_sqlmodel import get_session

from .schema import *


app=APIRouter(include_in_schema=True,prefix="/remit-banners",tags=['REMIT BANNER'])
@app.get('/',response_model=list[BannersRead])
async def all(db:Session=Depends(get_session)):
    return Banners.all(session=db)


@app.post('/')
async def create(url:str=None,image:UploadFile =File(...),db:Session=Depends(get_session)):
    file_content=await image.read()
    filename=image.filename
    upload_to_gcs(filename,file_content ,image.content_type)
 
    banner=Banners(url=url,image=filename)
    upload_to_gcs(filename,file_content,image.content_type)
    return Banners.create(banner,BannersBase, db)

@app.get('/{id}',response_model=BannersRead)
async def get_banner(id:int,db:Session=Depends(get_session)):
    return Banners.by_id(id,session=db)


@app.patch('/{id}',response_model=BannersRead)
async def update(id:int,hero:BannersUpdate,db:Session=Depends(get_session)):
    # hero.updated_at = datetime.utcnow()
 
    return Banners.update(BannersBase.by_id(id,session=db),hero,db)
 
@app.delete('/')
async def delete(id:int,db:Session=Depends(get_session)):
    return Banners.delete(BannersBase.by_id(id,session=db))