from enum import Enum
from sqlmodel import SQLModel

class SubscriptionType(str,Enum):
    MONTHLY="MONTHLY"
    YEARLY="YEARLY"
    WEEKLY="WEEKLY"
    DAILY="DAILY"
    HOURLY="HOURLY"
    
class SubscriptionBase(SQLModel):
    name:str
    type:SubscriptionType
    fee:float
    time:int
    
