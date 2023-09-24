from datetime import datetime,date
from typing import Optional
from sqlmodel import Column, DateTime, Field, SQLModel, func

from record_service.main import RecordService


class CarouselBase(SQLModel):
    image:str="string"
    link:str="string"
    title:str="string"
# class CarouselModel(CarouselBase):
#     pass

class Carousel(CarouselBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)

class CarouselCreate(CarouselBase):
    pass

class CarouselRead(CarouselBase):
    id:Optional[int] = Field(default=None, primary_key=True) 

class CarouselUpdate(CarouselBase):
    pass

class MovieBase(SQLModel):
    name:str="string"
    logo:str="test"
    trailer:str="test"
    url:str="test"
    price:float="43"
    rating:float="2"
    release_date:date="2023-03-02"
    created_at:Optional[datetime]=Field(sa_column=Column(DateTime,default=func.now()),default=datetime.now())
    updated_at:Optional[datetime]=Field(sa_column=Column(DateTime,default=func.now(),onupdate=func.now()),default=datetime.now())

 
class MovieCreate(MovieBase):
    pass
    # class Config:
    #     schema_extra = {
    #     "example":{
    #         "title":"sfe",
    #         "logo": "dger",
    #         "trailer": "sef",
           
    #         "price":"1.0",
    #         "rating": "4.7",
    #         "release_date":"2023-05-11",

    #         }
    #     }

class MovieRead(MovieBase):
    id:Optional[int] = Field(default=None, primary_key=True) 

class MovieUpdate(MovieBase):
    pass

class Movie(MovieBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 



class TVShowBase(SQLModel):
    title:str
    logo:str
    trailer:str
    url:str
    price:float
    rating:float
    release_date:datetime
    created_at:Optional[datetime]=Field(sa_column=Column(DateTime,default=func.now()),default=datetime.now())
    updated_at:Optional[datetime]=Field(sa_column=Column(DateTime,default=func.now(),onupdate=func.now()),default=datetime.now())

class TVShowRead(SQLModel):
    id:Optional[int] = Field(default=None, primary_key=True) 


class TVShowCreate(TVShowBase):
    pass

class TVShowRead(TVShowBase):
    id:Optional[int] = Field(default=None, primary_key=True) 

class TVShowUpdate(TVShowBase):
    pass

class TVShow(TVShowBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 

class EpisodeBase(SQLModel):
    title:str
    trailer:str
    url:str
    rating:float
    created_at:Optional[datetime]=Field(sa_column=Column(DateTime,default=func.now()),default=datetime.now())
    updated_at:Optional[datetime]=Field(sa_column=Column(DateTime,default=func.now(),onupdate=func.now()),default=datetime.now())


class EpisodeCreate(EpisodeBase):
    pass

class EpisodeRead(EpisodeBase):
    id:Optional[int] = Field(default=None, primary_key=True) 

class EpisodeUpdate(EpisodeBase):
    pass

    
class Episode(EpisodeBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 

class SubscriptionPlanBase(SQLModel):
    name:str
    price:float
    description:str
    billing_frequency:int

class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass

class SubscriptionPlanRead(SubscriptionPlanBase):
    id:Optional[int] = Field(default=None, primary_key=True) 

class SubscriptionPlanUpdate(SubscriptionPlanBase):
    pass

class SubscriptionPlan(SubscriptionPlanBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 

class SubscriptionBase(SQLModel):
    start_date:date
    end_date:date
    subscription_id:Optional[int]=Field(default=1, foreign_key="subscriptionplan.id")  
    user_id:Optional[int]=Field(default=1, foreign_key="remituser.id")  

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionRead(SubscriptionBase):
    id:Optional[int] = Field(default=None, primary_key=True) 

class SubscriptionUpdate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 

class PaymentBase(SQLModel):
    user_id :int
    subscriptoin_id:int
    amount:float
    payment_date:date
    payment_method:str

class PaymentCreate(PaymentBase):
    pass

class PaymentRead(PaymentBase):
    id:Optional[int] = Field(default=None, primary_key=True) 

class PaymentUpdate(PaymentBase):
    pass

class Payment(PaymentBase, RecordService, table=True):
    id:Optional[int] = Field(default=None, primary_key=True) 

    # subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    # amount = models.DecimalField(max_digits=10, decimal_places=2)
    # payment_date = models.DateTimeField(auto_now_add=True)
    # payment_method = models.CharField(max_length=255)  # Store the payment method (e.g., Stripe, PayPal)


# # Create your models here.
# class Plan(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     billing_frequency = models.IntegerField(default=1)  # Billing frequency in months
#     description = models.TextField()
#     # features = models.ManyToManyField('SubscriptionFeature')
#     def __str__(self) -> str:
#         return self.name

# class SubscriptionFeature(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name
    
# class Subscription(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     active = models.BooleanField(default=False)
#     STATUS_CHOICES = (
#         ('active', 'Active'),
#         ('canceled', 'Canceled'),
#         ('pending', 'Pending'),  # Add a 'Pending' status
#         ('suspended', 'Suspended'),  # Add a 'Suspended' status
#     )
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
#     @property
#     def is_active(self):
#         today = datetime.now().date()
#         return self.start_date <= today <= self.end_date
#     def __str__(self):
#         return self.plan.name+" Plan "+self.user.email + (" Active" if self.is_active else " Expired")
# class Payment(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_date = models.DateTimeField(auto_now_add=True)
#     payment_method = models.CharField(max_length=255)  # Store the payment method (e.g., Stripe, PayPal)

#     def __str__(self):
#         return f"{self.user.username} - {self.subscription.plan.name} - ${self.amount}"

