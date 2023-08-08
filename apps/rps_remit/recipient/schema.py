
from sqlmodel import SQLModel


class RecipientBase(SQLModel):
    recipient_type:str
    recipient_country:str
    currency:str
    relationship:str
    title:str
    first_name:str
    last_name:str
    email:str
    mobile:str
    address:str
    note:str
