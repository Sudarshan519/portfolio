from sqlmodel import SQLModel


class RemitDepostBase(SQLModel):
    name:str
    location:str
    phone:str
    mobile:str
    logo:str
    country:str
    