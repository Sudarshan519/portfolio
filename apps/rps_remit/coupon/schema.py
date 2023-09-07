

from typing import Optional
from sqlmodel import Field, SQLModel

from record_service.main import RecordService


class CouponBase(SQLModel):
    code:str
    is_flat:bool=True
    discount_amount:float
    discount_percentage:float
    max_usage_count:int=8
    single_usage:bool

class CouponRead(CouponBase):
    pass
class CouponCreate(CouponBase):
    pass

class CouponUpdate(CouponBase):
    pass
class Coupon(CouponBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 

class UseCouponBase(SQLModel):
    code:str
    user_id:int
    transaction_id:int
    usage_count:int



class UseCouponRead(UseCouponBase):
    pass
class UseCouponCreate(UseCouponBase):
    pass

class UseCouponCouponUpdate(UseCouponBase):
    pass
 
class UseCoupon(CouponBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 
