
from fastapi import FastAPI


app=FastAPI(title="SUBSCRIPTION APP",description="FASTAPI WITH POSTGRES")

@app.get("/hello")
async def hello():
    return {"detail":"hello from server side"}
async def getSubscriptionTypes():
    return {
        "available_subscriptions":[]
    }

async def subscribe(type:str):
    return {
        "status":"Subscribed for 1 months"
    }

async def unsubscribe(type:str):
    return {}

async def changeSubscriptionType(type:str):
    return {}