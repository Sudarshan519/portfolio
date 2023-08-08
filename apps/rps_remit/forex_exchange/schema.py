 
from datetime import date,datetime
from typing import Optional
from sqlmodel import Field, Session, SQLModel

from record_service.main import RecordService


class ForeignExchangeChargeBase(SQLModel):
 
    min_amount:float
    is_flat:bool 
    charge_upto_one_lakh:float=None
    carge_from_one_ten_lakh:float=None
    charge_from_ten_lakh_to_1core:float=None
    charge_upto_one_lakh_in_percentage:float=None
    charge_from_one_ten_lakh_in_percentage:float=None
    charge_from_ten_lakh_to_1core_in_percentage:float=None
    created_at:date=date.today()
    updated_at:datetime=datetime.now()
    cancellation_charge:float
    issuance_charge=float



class ForexExchangeCreate(ForeignExchangeChargeBase):
    pass

class ForexExchangeRead(ForeignExchangeChargeBase):
    id:Optional[int] = Field(default=None, primary_key=True) 

class ForexExchangeUpdate(ForeignExchangeChargeBase):
    pass

 
class ForexExchange(ForeignExchangeChargeBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 
