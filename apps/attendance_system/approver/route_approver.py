from fastapi import APIRouter
from pydantic import BaseModel


class BaseAttendanceUser(BaseModel):
    phone:str
    otp:str


router =APIRouter(include_in_schema=True,prefix='/approver',tags=['Approver'])

@router.post('/')
async def create_approver():
    pass