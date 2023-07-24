from fastapi import FastAPI, HTTPException, Request
import redis as aioredis
import json
import requests

app = FastAPI()
redis_pool = None

async def get_redis_pool():
    global redis_pool
    if redis_pool is None:
        redis_pool = await aioredis.create_redis_pool("redis://127.0.0.1:6379")
    return redis_pool
@app.get('')
async def hello():
    return "hello"
@app.post("/webhook/")
async def webhook_handler(request: Request):
    try:
        data = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    try:
        redis = await get_redis_pool()
        await redis.lpush("webhook_data", json.dumps(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Data received and stored successfully"}

def send_notification(notification_url, notification_payload):
    try:
        response = requests.post(notification_url, json=notification_payload)

        if response.ok:
            print("Notification sent successfully.")
        else:
            print(f"Failed to send notification. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send notification: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# from fastapi import FastAPI, HTTPException, Request
# import json
# import redis as aioredis

# app = FastAPI()
# import asyncio

# class CustomError(aioredis.RedisError):
#     # Your custom error implementation here
#     pass

# # In a real-world scenario, you'd have better configurations for Redis connection.
# REDIS_HOST = "localhost"
# REDIS_PORT = 6379

# # Create a connection pool to Redis
# def get_redis_pool():
#     return aioredis.create_redis_pool(f"redis://{REDIS_HOST}:{REDIS_PORT}")

# @app.post("/webhook")
# def process_webhook(request: Request):
#     # Parse the JSON data sent by the payment provider
#     data = request.json()

#     # In a production system, you should validate the data received from the webhook
#     # and implement appropriate security checks.

#     # Store the payment data in Redis
#     redis_pool = get_redis_pool()
#     try:
#         redis_pool.lpush("payments", json.dumps(data))
#     except CustomError as e:
#         print(e)
#         pass
#     finally:
#         redis_pool.close()
#         redis_pool.wait_closed()

#     return {"message": "Webhook received successfully."}

# @app.get("/payments")
# async def get_payments():
#     # Retrieve all payments stored in Redis
#     redis_pool = get_redis_pool()
#     try:
#         payments = redis_pool.lrange("payments", 0, -1)
#         # Decode the bytes and convert to JSON
#         return [json.loads(payment.decode()) for payment in payments]
#     finally:
#         redis_pool.close()
#         redis_pool.wait_closed()
