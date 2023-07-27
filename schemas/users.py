from typing import Optional
from pydantic import BaseModel,EmailStr

class UserBaseSchema(BaseModel):
    # name: str
    email: EmailStr
    # photo: str

    class Config:
        orm_mode = True
#properties required during user creation
class UserCreate(UserBaseSchema):
    # username: str
    # email : EmailStr
    password : str
    # is_employer:Optional[bool]
    # class Config():  #tells pydantic to convert even non dict obj to json
    #     orm_mode = True

class ShowUser(BaseModel):   #new
    username : str=None
    email : EmailStr='test@test.com'
    is_active : bool=False

    class Config():  #tells pydantic to convert even non dict obj to json
        orm_mode = True


class UserResponse(UserBaseSchema):
    pass
    id: int
    # created_at: datetime
    # updated_at: datetime
