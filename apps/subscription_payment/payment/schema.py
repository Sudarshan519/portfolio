from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel

from apps.subscription_payment.admin.schema import SubscriptionBase
class PaymentStatus(str,Enum):
    PENDING="PENDING"
    PAID="PAID"

class PaymentBase(SQLModel):
    user_id:int
    name:str
    subscription_id:int
    fee:float
    time:int
    status:PaymentStatus
    created_at:datetime
    updated_at:datetime=None
    due_date:datetime
    coupon_id:int=None
    tax:float



class PaymentCreate(PaymentBase):
    pass

class PaymentRead(PaymentBase):
    id:Optional[int] = Field(default=None, primary_key=True) 

class PaymentUpdate(PaymentBase):
    pass
