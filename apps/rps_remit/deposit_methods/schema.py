from sqlmodel import SQLModel


class DepositMethods(SQLModel):
    deposit_type:str
    deposit_date:str
    amount:str
    slip:str
    remarks:str
    source_of_fund:str
