from sqlmodel import SQLModel


class JapanBankBase(SQLModel):
    name:str
    account_number:str
    contact:str
    address:str
    currency:str
    total_balance:float

class NepalBankBase(SQLModel):
    name:str
    account_number:str
    contact:str
    address:str
    currency:str
    total_balance:float
