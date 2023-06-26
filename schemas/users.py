from typing import Optional
from pydantic import BaseModel,EmailStr


#properties required during user creation
class UserCreate(BaseModel):
    # username: str
    email : EmailStr
    password : str
    # is_employer:Optional[bool]
    class Config():  #tells pydantic to convert even non dict obj to json
        orm_mode = True

class ShowUser(BaseModel):   #new
    username : str=None
    email : EmailStr='test@test.com'
    is_active : bool=False

    class Config():  #tells pydantic to convert even non dict obj to json
        orm_mode = True