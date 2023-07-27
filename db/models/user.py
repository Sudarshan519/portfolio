from enum import Enum
from sqlalchemy import Column,Integer, String,Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from pydantic import BaseModel

class User(Base):
    id = Column(Integer,primary_key=True,index=True)
    # username = Column(String(60),unique=True,nullable=False)
    email = Column(String(60),nullable=False,unique=True,index=True)
    hashed_password = Column(String(256),nullable=False)
    is_active = Column(Boolean(),default=True)
    verified=Column(Boolean,default=True)
    is_superuser = Column(Boolean(),default=False)

