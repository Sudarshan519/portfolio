from sqlmodel import SQLModel


class RecivingMethodBase(SQLModel):
    payment_mode:str
    name:str=None
    account_number:str=None
    pickup_address:str=None
