



from sqlmodel import Column, Field, SQLModel, String


class SubscriptionUserBase(SQLModel):
    # id: Column(Integer,primary_key=True,index=True)
    username :str=''# Column(String(60),unique=True,nullable=False)
    email :str
    phone:str=Field(default=None,sa_column=Column(String(16),nullable=True,)) 
    photo :str=''
    phone_verified:bool=False
    hashed_password: str
    is_active: bool=False
    verified:bool=False
    # full_kyc=Column(Boolean,default=False)
    is_superuser: bool=False
    is_staff:bool=False
    role:str=''