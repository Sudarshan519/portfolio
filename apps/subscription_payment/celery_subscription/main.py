# from fastapi import FastAPI
# from celery import Celery
# from datetime import datetime, timedelta

# app = FastAPI()

# # Celery Configuration
# celery = Celery(
#     "subscription_app",
#     broker="redis://localhost:6379/0",
#     backend="redis://localhost:6379/0"
# )

# # Subscription Model (Assuming SQLAlchemy ORM for the database)
# from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Subscription(Base):
#     __tablename__ = "subscriptions"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer)
#     start_date = Column(DateTime)
#     next_billing_date = Column(DateTime)
#     is_active = Column(Boolean, default=True)
#     is_paused = Column(Boolean, default=False)

# # API Endpoints
# @app.post("/start_subscription")
# async def start_subscription(user_id: int):
#     # Create a new subscription entry in the database
#     start_date = datetime.now()
#     next_billing_date = start_date + timedelta(days=30)  # Assuming monthly billing
#     subscription = Subscription(user_id=user_id, start_date=start_date, next_billing_date=next_billing_date)
#     session = Session()
#     session.add(subscription)
#     session.commit()
#     session.close()

#     # Schedule the subscription processing task
#     process_subscription.apply_async((subscription.id,), eta=next_billing_date)

#     return {"message": "Subscription started successfully"}

# @app.post("/pause_subscription")
# async def pause_subscription(subscription_id: int):
#     # Update the subscription status to paused
#     subscription = Session().query(Subscription).filter(Subscription.id == subscription_id).first()
#     if subscription:
#         subscription.is_paused = True
#         Session().commit()
#         Session().close()
#         return {"message": "Subscription paused successfully"}
#     return {"message": "Subscription not found"}

# @app.post("/resume_subscription")
# async def resume_subscription(subscription_id: int):
#     # Update the subscription status to active
#     subscription = Session().query(Subscription).filter(Subscription.id == subscription_id).first()
#     if subscription:
#         subscription.is_paused = False
#         Session().commit()
#         Session().close()
#         return {"message": "Subscription resumed successfully"}
#     return {"message": "Subscription not found"}

# @app.post("/cancel_subscription")
# async def cancel_subscription(subscription_id: int):
#     # Update the subscription status to canceled
#     subscription = Session().query(Subscription).filter(Subscription.id == subscription_id).first()
#     if subscription:
#         subscription.is_active = False
#         Session().commit()
#         Session().close()
#         return {"message": "Subscription canceled successfully"}
#     return {"message": "Subscription not found"}

# # Celery Task for Subscription Processing
# @celery.task
# def process_subscription(subscription_id):
#     subscription = Session().query(Subscription).filter(Subscription.id == subscription_id).first()
#     if subscription and subscription.is_active and not subscription.is_paused:
#         # Perform the subscription calculation and billing logic here
#         # Update the next billing date, and schedule the task again for the next billing cycle
#         subscription.next_billing_date += timedelta(days=30)
#         Session().commit()
#         Session().close()
#         process_subscription.apply_async((subscription.id,), eta=subscription.next_billing_date)