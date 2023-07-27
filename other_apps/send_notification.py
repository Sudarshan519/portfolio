import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
import asyncio
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import redis
app = FastAPI()

# Store all connected WebSocket clients and their subscriptions
websocket_clients = {}
subscriptions = {}

templates = Jinja2Templates(directory="templates")
# async def get_redis_pool():
#     global redis_pool
#     if redis_pool is None:
#         redis_pool = await redis.create_redis_pool("redis://127.0.0.1:6379")
#     return redis_pool
@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str):
    await websocket.accept()

    # Store the WebSocket and the corresponding channel to which it is subscribed
    websocket_clients[websocket] = channel

    try:
        # Create a new list to store WebSocket clients subscribed to this channel
        if channel not in subscriptions:
            subscriptions[channel] = []

        # Subscribe the WebSocket client to the requested channel
        subscriptions[channel].append(websocket)

        while True:
            # Wait for incoming messages from the client (optional)
            message = await websocket.receive_text()
            print(f"Received message: {message}")

    except WebSocketDisconnect:
        # Remove the WebSocket client and unsubscribe from the channel when it disconnects
        channel = websocket_clients[websocket]
        subscriptions[channel].remove(websocket)
        del websocket_clients[websocket]

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("notification.html", {"request": request})
class MessageData(BaseModel):
    message: str
@app.post("/send_message/{channel}")
async def send_message(channel: str, message_data: MessageData):
    message = message_data.message
    print(message)
    # Send the message to all WebSocket clients subscribed to the specified channel
    if channel in subscriptions:
        print(channel)
        for websocket in subscriptions[channel]:
            print(message)
            await websocket.send_text(json.dumps(message_data.dict()))

    return {"message": "Message sent successfully!"}