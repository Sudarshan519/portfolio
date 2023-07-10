# build a schema using pydantic
import json
from typing import Optional,List
from pydantic import BaseModel
 
class CustomObject(BaseModel):
    name:str
    age:str
    contact:str
    class Config:
        orm_mode =True
from fastapi import File, UploadFile
class Author(BaseModel):
    name:str
    age:int
    contacts:Optional[List[CustomObject]]
    file:UploadFile=File(...)
    @classmethod
    def __get_validators__(cls) :
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls,value): 
        if isinstance(value,str):
            return cls(**json.loads(value))
        return value
    class Config:
        orm_mode = True
class ContactDict(BaseModel):
    data:List[Author]
    class Config:
        orm_mode =True
        
class ExtraDataDict(BaseModel):
    data:List[Author]
    class Config:
        orm_mode = True
        
    # @classmethod
    # def validate_to_json(cls,value):
    #     if isinstance(value,str):
    #         return cls(**json.loads(value))
    #     return value
class Book(BaseModel):
    title: str
    rating: int
    author_id: int
    author: Author
    class Config:
        orm_mode = True



class BookView(BaseModel):
    title:str
    