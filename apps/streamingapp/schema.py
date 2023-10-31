

from datetime import datetime
from pyparsing import Optional
from sqlmodel import SQLModel
from sqlmodel import Column, DateTime, Enum, Field, Relationship, SQLModel, func

class Carosuel(SQLModel):
    logo:str

class Movie(SQLModel):
    title:str
    logo:str
    url:str
    trailer:str
    desc:str
    movie_path:str
    price:str
    rating:float
    discount:float
    trending:str
    created_at:Optional[datetime]=Field(sa_column=Column(DateTime,default=func.now()),default=datetime.now())
    updated_at:Optional[datetime]=Field(sa_column=Column(DateTime,default=func.now(),onupdate=func.now()),default=datetime.now())

    
class TvShow(SQLModel):
    title:str
    logo:str
    url:str
    trailer:str
    desc:str
    movie_path:str
    price:str
    rating:float
    discount:float
    trending:str
    created_at:Optional[datetime]=Field(sa_column=Column(DateTime,default=func.now()),default=datetime.now())
    updated_at:Optional[datetime]=Field(sa_column=Column(DateTime,default=func.now(),onupdate=func.now()),default=datetime.now())
# upload_to_gcs(filename,file_content,image.content_type)


class Episodes(SQLModel):
    title:str
    logo:str
    url:str
    trailer:str
    desc:str
    movie_path:str
    created_at:Optional[datetime]=Field(sa_column=Column(DateTime,default=func.now()),default=datetime.now())
    updated_at:Optional[datetime]=Field(sa_column=Column(DateTime,default=func.now(),onupdate=func.now()),default=datetime.now())