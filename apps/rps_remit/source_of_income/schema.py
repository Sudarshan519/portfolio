from sqlmodel import SQLModel


class SourceOfIncomeBase(SQLModel):
    name:str