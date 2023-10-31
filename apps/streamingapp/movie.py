from typing import Optional
from fastapi import APIRouter, Body, Depends, FastAPI, File, Form, HTTPException, UploadFile
from apps.rps_remit.gs_cloud_storage import generate_signed_url, upload_to_gcs
from apps.streamingapp.schema import *
from db.session_sqlmodel import get_session, init_db
from sqlmodel import Field, Session, SQLModel, create_engine, select
# from ..currency_router import app as currencyapp

app=APIRouter(prefix='/movie',tags=["REMIT MOVIE"] )

@app.get('/',response_model=list[MovieRead])
async def all(db:Session=Depends(get_session)):
    return Movie.all(session=db)

@app.post('/')
async def create(movie:MovieCreate=Form(...) ,moviefile:UploadFile=None, db:Session=Depends(get_session)):
    # print(movie)
    # print(moviefile)
    # return movie
    if moviefile:

        print(moviefile.filename)
        file_content=await moviefile.read()
        
        # contents = moviefile.file.read()
        # with open("media/"+moviefile.filename, 'wb') as f:
        #     f.write(contents)
        filename=moviefile.filename
        url= upload_to_gcs(filename,file_content ,moviefile.content_type)
        print(url)
        movie.url=url
        print(movie)
    return Movie.create(movie,MovieBase, db)

@app.get('/{id}',response_model=MovieRead)
async def get_hero(id:int,db:Session=Depends(get_session)):
    return Movie.by_id(id,session=db)


@app.patch('/{id}',response_model=MovieRead)
async def update(id:int,hero:MovieUpdate=Form(...),moviefile:UploadFile=None,db:Session=Depends(get_session)):
 
    if moviefile:
        print(moviefile.filename)
        file_content=await moviefile.read()
        filename=moviefile.filename
        url= upload_to_gcs(filename,file_content ,moviefile.content_type)
        print(url)
        hero.url=url
        print(hero)
    return Movie.update(Movie.by_id(id,session=db),hero,db)
 
@app.delete('/')
async def delete(id:int,db:Session=Depends(get_session)):
    return Movie.delete(Movie.by_id(id,session=db))

@app.get("/watch-movie/{id}")
async def watch_movie(id,db:Session=Depends(get_session)):
    movie=Movie.by_id(id,db)
    return {"data":{"url":generate_signed_url(movie.url)}}