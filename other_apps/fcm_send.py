from fastapi import APIRouter, BackgroundTasks
import requests
import json

reqUrl = "https://fcm.googleapis.com/fcm/send"

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)",
 "Authorization": "Bearer AAAAfg4K7Zg:APA91bH64IBqL3YLRipSjH7OZ8qpWObmQYEZb7APgZ76ohlRf8JnUewDz-zBNXTQRSIoYEQIV6v7evWnp6jqw-vcfMfRnwGQvuqUptDI4CwKsSewNmzNdvMPqZIQpJzyLODyLwQdW3vM",
 "Content-Type": "application/json" 
}
headersList1={
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)",
 "Authorization": "Bearer AAAAYxii3ME:APA91bHaL6f9iVj00fF8agpP8TN7R5WsWLgHUJ8DgEBRzGExxmyNpwR8bCQhW8Wxzm3bodhHshfie_8QsoKtd2HUbtxUSW5NtPftWbcuenyj6ZY7ZdgJCvX_KiZKzBPESTKqPDpVbpm7",
 "Content-Type": "application/json" 
}
token="AAAAVWtqYtY:APA91bGY_1xbTjOAWzjJgWYrFKTT5tGil6PSd43uvenm1_D39lYrJQ5Nvw66INpcW0nJ-duebfRKZQe7I-3CZ3DkPlWiY-0ISG-XGkBQT5doN5QfKnUrLg45O6CaP5mJFE-BnQ7v9yHh"
headers={
     "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)",
 "Authorization": f"Bearer {token}",
 "Content-Type": "application/json" 
}
# payload = json.dumps( {
#       "to": "",
#       "notification": {
#         "body": "Urgent!!! $userName requires",
#         "title": "Blood Required"
#       }
#     })

# response = requests.request("POST", reqUrl, data=payload,  headers=headersList)

# print(response.text)
# function that will run in background after sending the response
def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)

app=APIRouter()
@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Tasks are happening in background"}

class NotificationService:
    @staticmethod
    def send_notification(title:str,message:str,to:str=None,id:int=None,status:str=None):
        reqUrl = "https://fcm.googleapis.com/fcm/send"

# hajir client token 
    #   SDLFJIEW  hajir_client="fc7Qv0RITM-sh1YTeFGuV-:APA91bE48uJf7I_eFAcKCuVyL3r12fUZx5hqBA8c6THs9XU5afu9_wSie1a17_HR8N8SEo5Y-XVQVI-X_6GeUk5vKsTSp7YiLUErND8GK-TZcpChJwsHzXMCkSItHp6LvXan1ncq3L8X&&& UPDATE"LIJE
        payload = json.dumps( {
              # "to": "",
               "to":to,#"dUzGdt5-QXqwda56ASjOJg:APA91bEwBfwRJoIEXPffZ0JBytbvTc6UGdcLSuNE04rrsaOFpqqaPofYlHAswxqJn2pDLPUT4Y5F-fm35GnMl5Ph7cCF-g6_Fhj_Qc-CfMW4F1k_nYC6hgVy3o_tCPe0XbPpYXK2u6UL",
               "data":{
       "id":id,
       "status":status
      }, "notification": {
                "body": message,
                "title": title,
                
              }
            })
        response = requests.request("POST", reqUrl, data=payload,  headers=headersList1)
        print(response.content)