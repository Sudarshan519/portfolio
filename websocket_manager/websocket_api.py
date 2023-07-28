# import asyncio
# import datetime
# import json
# from fastapi import WebSocket, WebSocketDisconnect
# from fastapi.encoders import jsonable_encoder
# from fastapi.params import Depends
# from fastapi import APIRouter
# from requests import Session
# from db.models.attendance import EmployeeModel
# from websocket_manager.manager import ws_manager
# from db.session import get_db

# notificationRoute = APIRouter(prefix='',tags=[])
# # webapp_router.include_router(route_index.router, prefix="", tags=["job-webapp"])

# @notificationRoute.websocket("/ws/{user_id}")
# async def websocket_endpoint(websocket: WebSocket,user_id:str, db: Session = Depends(get_db) ):
#     # print(user_id)
#     list=[]
#     employee=db.query(EmployeeModel).limit(5).all()

#     for e in employee:
#          list.append(jsonable_encoder(e))
#     # print(list)
#     #     print(e.as_dict())
#     # with Session(engine) as session:
#     #     statement = select(Poll).where(Poll.id == poll_id)
#     #     poll = session.exec(statement).first()
#     #     if poll is None:
#     #         await websocket.close()
#     #         return
#     await websocket.accept()
#     # print(TActiveConnections)
#     await ws_manager.connect(user_id, websocket)
#     await ws_manager.send_message(user_id,({
        
#         "server":"Hello from server","employee":jsonable_encoder(list)}))
#     try:
#         while True:
#             # await asyncio.sleep(0.1)
#             await websocket.receive_json()
#     except WebSocketDisconnect:

#         await ws_manager.disconnect(user_id, websocket)

# @notificationRoute.post('/send/')
# async def send_message( db: Session = Depends(get_db)):
#     print(ws_manager.connections())
#     for k,v in ws_manager.connections().items():
#         employee=db.query(EmployeeModel).limit(5).all()
#         print(k)
#         await ws_manager.send_message(k,{
#             "time":str(datetime.datetime.now()),
#             "server":"Hello from server","employee":jsonable_encoder(employee)})
#         return 'success'
    