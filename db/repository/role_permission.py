
from ctypes import Union
 
import select
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel,Field
from pyparsing import Optional
from requests import Session
from db.base import Base
from db.models.user import Permissions
from typing import Optional

from sqlmodel import Field, SQLModel

from db.session import get_db

class ActiveRecord(SQLModel):
    @classmethod
    def by_id(cls, id: int, session):
        obj = session.get(cls, id)
        if obj is None:
            raise HTTPException(status_code=404, detail=f"{cls.__name__} with id {id} not found")
        return obj

    @classmethod
    def all(cls, session):
        return session.exec(select(cls)).all()

    @classmethod
    def create(cls, source: dict  , SQLModel, session):
        if isinstance(source, SQLModel):
            obj = cls.from_orm(source)
        elif isinstance(source, dict):
            obj = cls.parse_obj(source)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def save(self, session):
        session.add(self)
        session.commit()
        session.refresh(self)

    def update(self, source: dict| SQLModel, session):
        if isinstance(source, SQLModel):
            source = source.dict(exclude_unset=True)

        for key, value in source.items():
            setattr(self, key, value)
        self.save(session)

    def delete(self, session):
        session.delete(self)
        session.commit()

class RoleBase(BaseModel):
    name: str 

class RoleCreate(RoleBase):
    pass


class Role(RoleBase, ActiveRecord ):
    id: int=None


class PermissionBase(BaseModel):
    name:str

class PermissionCreate(PermissionBase):
    pass

class RoleService:
    @staticmethod
    def createPermission(permission:Permissions,db):
        db.add(permission)
        db.commit(permission)
        db.refresh(permission)
        return permission
    # @staticmethod
    # def createRole(role:RoleBase,db):
    #     Role.create(role,db)
