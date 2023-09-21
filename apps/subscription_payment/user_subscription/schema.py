from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel

from apps.subscription_payment.subscription.schema import SubscriptionBase
 
class SubscriptionStatus(Enum):
    ACTIVE="ACTIVE"
    INACTIVE="INACTIVE"
class UserSubscriptionBase(SQLModel):
    user_id:int
    name:str
    subscription:SubscriptionBase
    fee:float
    time:int
    created_date:datetime
    due_amount:float
    @property
    def status(self):
        return True


