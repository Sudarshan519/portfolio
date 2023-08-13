

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