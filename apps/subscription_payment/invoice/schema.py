

from sqlmodel import SQLModel

from apps.subscription_payment.payment.schema import PaymentStatus


class InvoiceBase(SQLModel):
    user_id:int
    name:str
    subscription_id:int
    fee:float
    time:int
    status:PaymentStatus
    