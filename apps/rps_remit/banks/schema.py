from sqlmodel import SQLModel


class BankBase(SQLModel):
    name:str
    account_number:str
    contact:str
    
