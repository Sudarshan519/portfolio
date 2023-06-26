# build a schema using pydantic
from pydantic import BaseModel



class Author(BaseModel):
    name:str
    age:int

    class Config:
        orm_mode = True
        


class Book(BaseModel):
    title: str
    rating: int
    author_id: int
    author: Author
    class Config:
        orm_mode = True



class BookView(BaseModel):
    title:str
    