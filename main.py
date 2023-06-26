# from fastapi import FastAPI
# from pydantic import BaseModel
# from dotenv import load_dotenv

# load_dotenv('.env')


# # To run locally
# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8000)
# app = FastAPI()
# # to avoid csrftokenError
# app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

# class Msg(BaseModel):
#     msg: str


# @app.get("/")
# async def root():
#     return {"message": "Hello World. Welcome to FastAPI!"}


# @app.get("/path")
# async def demo_get():
#     return {"message": "This is /path endpoint, use a post request to transform the text to uppercase"}


# @app.post("/path")
# async def demo_post(inp: Msg):
#     return {"message": inp.msg.upper()}


# @app.get("/path/{path_id}")
# async def demo_get_path_id(path_id: int):
#     return {"message": f"This is /path/{path_id} endpoint, use post request to retrieve result"}


import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import Book as SchemaBook
from schema import Author as SchemaAuthor

from schema import Book
from schema import Author

from models import Book as ModelBook
from models import Author as ModelAuthor

import os
from dotenv import load_dotenv
import motor.motor_asyncio
load_dotenv('.env')

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.college
# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URI'])

@app.get("/")
async def root():
    return {"message": "hello world"}


@app.post('/book/', response_model=SchemaBook)
async def book(book: SchemaBook):
    db_book = ModelBook(title=book.title, rating=book.rating, author_id = book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book

@app.get('/book/')
async def book():
    book = db.session.query(ModelBook).all()
    return book


  
@app.post('/author/', response_model=SchemaAuthor)
async def author(author:SchemaAuthor):
    db_author = ModelAuthor(name=author.name, age=author.age)
    db.session.add(db_author)
    db.session.commit()
    return db_author

@app.get('/author/')
async def author():
    author = db.session.query(ModelAuthor).all()
    return author


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)