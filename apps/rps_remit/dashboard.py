from ast import List
from fastapi import APIRouter,Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.models.user import User
from db.session import get_db


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
@router.get('/users',response_model=list[UserSchema])
def all_users(db:Session=Depends(get_db)):
   return db.query(User).filter(User.is_superuser==False).all()