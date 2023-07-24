from typing import Dict, Any, Set
from fastapi import WebSocket

TMessagePayload = Any
TActiveConnections = Dict[str, Set[WebSocket]]


class WSManager:
    _instance = None
    def __init__(self):
        self.active_connections: TActiveConnections = {}
    # def __new__(cls):
    #     if cls._instance is None:
    #         print('Creating the object')
    #         cls._instance = super(WSManager, cls).__new__(cls)
    #     return cls._instance
    async def connect(self, poll_id: str, ws: WebSocket):
        try:
            self.active_connections.setdefault(poll_id, set()).add(ws)
            
            print(self.active_connections)
        except Exception as e:
            print(e)

        # print(self.active_connections)
    def connections(self):
         return self.active_connections
    async def disconnect(self, poll_id: str, ws: WebSocket):
            print(poll_id)
        # if self.active_connections.get(poll_id):
            self.active_connections[poll_id].remove(ws)

    async def send_message(self, poll_id: str, message: TMessagePayload):
        # print(self.active_connections)#.get(poll_id, []))
        for ws in self.active_connections.get(poll_id, []):
            print(ws)
            await ws.send_json(message)


ws_manager = WSManager()