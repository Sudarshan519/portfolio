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


from typing import Annotated, Optional
from requests import Session
import uvicorn
from fastapi import Depends, FastAPI, File, HTTPException, Response, UploadFile,status
from fastapi_sqlalchemy import DBSessionMiddleware, db
from core.hashing import Hasher
from db.base import Base
from db.models.user import User
from get_rates import get_rates

from schemas.schema import Book as SchemaBook
from schemas.schema import Author as SchemaAuthor

from schemas.schema import Book
from schemas.schema import Author

from models import Book as ModelBook, FileModel
from models import Author as ModelAuthor
from db.session import engine   #new
import os
from dotenv import load_dotenv
import motor.motor_asyncio
from schemas.users import UserCreate
from core.config import settings
from upload_file import firebase_upload
from webapps.base import webapp_router
from fastapi import FastAPI, Form
import api  as mongorouter
from fastapi.staticfiles import StaticFiles
def get_user(username:str,db: Session)->User:
    user = db.query(User).filter(User.email == username).first()
 
    return user
load_dotenv('.env')
def create_tables():           #new
	Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(webapp_router)  #new
app.include_router(mongorouter.app)
app.mount("/static", StaticFiles(directory="static"), name="static")
# from starlette_validation_uploadfile import ValidateUploadFileMiddleware
# #add this after FastAPI app is declared 
# app.add_middleware(
#         ValidateUploadFileMiddleware,
#         app_path="/",
#         max_size=1048576, #1Mbyte
#         file_type=["text/plain"]
# )

create_tables()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URI"])
db_mongo = client.college
# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['POSTGRES_URL'])
@app.get('/forms/')
async def post(username:list[Annotated[str, Form()]]):
    pass
@app.get("/")
async def root():
    return {"message": "hello world"}

@app.get('/contacts')
async def get_contacts():
    contacts = await db_mongo["contact"].find().to_list(100)
    return contacts

@app.get('/files',response_model=list[FileModel])
async def get_files():
    contacts = await db_mongo["files"].find().to_list(100)
    return contacts

@app.post('/book/', response_model=SchemaBook)
async def book(book: SchemaBook):
    db_book = ModelBook(title=book.title, rating=book.rating, author_id = book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book

@app.get('/book/',response_model=list[Book])
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

@app.get('/exchange-rates/')
async def get_exchanges_rates():
    rates=  get_rates()
    return rates

# @app.get('/images/')
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

from fastapi import File, UploadFile
from typing import List
from fastapi.encoders import jsonable_encoder
@app.post("/upload",)
async def upload(author:Author,files:Optional[ List[UploadFile]] = File(None)):
    print(author)
    urls=[]
    for file in files:
        try:
            #TO CHECK IF FILE IS LARGER THAN * MB
            if len(await file.read()) >= 8388608:
                return {"Your file is more than 8MB"}
           
            ext=file.filename.split(".")[-1]
            #     filename=file.filename
                # TO WRITE CONTENTS IN SERVER
                # while contents := file.file.read(1024 * 1024):
                    # f.write(contents)
            url=firebase_upload(file.file.read(),ext,file.filename)
            urls.append(url)
        except Exception:
            return {"message": "There was an error uploading the file(s)"}
        # finally:
            # file.file.close()
        print(urls)
    for url in urls:
        result=await db_mongo['files'].insert_one(  jsonable_encoder (FileModel(url=url)))    
    return {"message": f"Successfuly uploaded {[url for url in urls]}"}
        #[file.filename for file in files]
@app.post('/forgot-password')
async def forgot_password(email:str):

    # TODO : ??SEND EMAIL
    return {"message":"Reset password link sent to email."}
@app.post('/reset-password/{str}')
async def reset_password(link:str,password:str):
    user = get_user(id=link,db=db) 
    user.hashed_password=Hasher.get_password_hash(user.password)
    return {"message":"Password Updated Sucessfully."}                                              
@app.post('/register',)
async def create_user(user:UserCreate):
    try:
        user = User( 
            email = user.email,
            hashed_password=Hasher.get_password_hash(user.password),
            is_active=True,
            is_superuser=False)
        
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Email already registered.")
from db.session import get_db    
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from utils import OAuth2PasswordBearerWithCookie    #new
from jose import JWTError, jwt
from datetime import timedelta
from core.security import create_access_token

def authenticate_user(username: str, password: str,db: Session):
    user = get_user(username=username,db=db) 
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user

@app.post("/token", )#response_model=Token)
def login_for_access_token(response: Response,form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):  #added response as a function parameter
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(key="name",value=user.email,httponly=False)
    response.set_cookie(key="access_token",value=f"Bearer {access_token}",httponly=True
                        )  #set HttpOnly cookie in response

    return {"access_token": access_token, "token_type": "Bearer"}


# @app.post('/login')
# async def login(user:UserCreate):
#     try:
#         pass
#     except Exception as e:
#         pass
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")
def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
 
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == username).first()
    if user is None:
        raise credentials_exception
    return user

# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

# def create_tables():           #new
# 	Base.metadata.create_all(bind=engine)
# def start_application():
# 	app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
# 	# include_router(app)
# 	# configure_static(app)
# 	# add_pagination(app)
# 	# create_tables()       #new
# 	return app

# app = start_application()
