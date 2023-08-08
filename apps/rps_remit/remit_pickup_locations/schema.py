from sqlmodel import SQLModel


class CashPickUpBase(SQLModel):
    name:str
    address:str
    phone:str
