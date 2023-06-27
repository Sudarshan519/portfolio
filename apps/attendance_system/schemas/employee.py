from typing import Optional
from pydantic import BaseModel,root_validator
from datetime import date,datetime

class EmployeeBase(BaseModel):
    title : Optional[str] = None
    company : Optional[str] = None
    location : Optional[str] = "Remote"
    description : Optional[str] = None
    salary: int
    date_added : Optional[date] = datetime.now().date()
    date_updated:Optional[date]=date
    @root_validator
    def number_validator(cls, values):
        values["updated_at"] = datetime.now()
        return values
    