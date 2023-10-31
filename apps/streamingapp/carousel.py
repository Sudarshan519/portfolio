from typing import Optional
from fastapi import APIRouter, Depends, FastAPI, Form, HTTPException, UploadFile
from apps.streamingapp.schema import *
from db.session_sqlmodel import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select
# from ..currency_router import app as currencyapp

app=APIRouter(prefix='/carousel',tags=["REMIT Carousel"] )
class FileManager:
    @staticmethod 
    def copyfile(image,filename,contentType):
        path=f"media/carousel/{datetime.now().microsecond}"+filename
        with open(path,'wb')as file:
            while contents := image.read(1024 * 1024):
                file.write(contents)

        return path


@app.get('/',response_model=list[CarouselRead])
async def all(db:Session=Depends(get_session)):
    return Carousel.all(session=db)

@app.post('/')
async def create(hero:CarouselCreate=Depends() ,image:UploadFile=None, db:Session=Depends(get_session)):

    filepath=FileManager.copyfile(image.file,image.filename,image.content_type)
    hero.image=filepath
    
    return Carousel.create(hero,CarouselBase, db)

@app.get('/{id}',response_model=CarouselRead)
async def get_hero(id:int,db:Session=Depends(get_session)):
    return Carousel.by_id(id,session=db)


@app.patch('/{id}',response_model=CarouselRead)
async def update(id:int,hero:CarouselUpdate,db:Session=Depends(get_session)):
 
 
    return Carousel.update(Carousel.by_id(id,session=db),hero,db)
 
@app.delete('/')
async def delete(id:int,db:Session=Depends(get_session)):
    return Carousel.delete(Carousel.by_id(id,session=db))