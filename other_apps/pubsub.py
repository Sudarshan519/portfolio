# from fastapi import FastAPI, WebSocket
# import redis

# app = FastAPI()

# # Connect to Redis
# redis_client = redis.Redis(host='localhost', port=6379)

# # Create a Redis pubsub instance
# pubsub = redis_client.pubsub()

# # Store all connected WebSocket clients and their subscriptions
# websocket_clients = {}
# subscriptions = {}

# @app.websocket("/ws/{channel}")
# async def websocket_endpoint(websocket: WebSocket, channel: str):
#     await websocket.accept()
#     websocket_clients[websocket] = channel
#     try:
#         # Subscribe the WebSocket client to the requested channel
#         pubsub.subscribe(channel)
        
#         # Process incoming messages from Redis and send them to the WebSocket client
#         for message in pubsub.listen():
#             if message['type'] == 'message' and message['channel'] == channel:
#                 await websocket.send_text(message['data'])
#     except:
#         # Unsubscribe the WebSocket client from the Redis channel when it disconnects
#         if websocket in websocket_clients:
#             channel = websocket_clients[websocket]
#             pubsub.unsubscribe(channel)
#             del websocket_clients[websocket]

# @app.post("/subscribe/{channel}")
# async def subscribe_channel(channel: str):
#     # Check if the channel exists before allowing subscription
#     if channel not in subscriptions:
#         # Create a new list to store WebSocket clients subscribed to this channel
#         subscriptions[channel] = []
    
#     return {"message": "Channel subscribed successfully!"}
