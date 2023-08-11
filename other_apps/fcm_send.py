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
    def send_notification(title:str,message:str):
        reqUrl = "https://fcm.googleapis.com/fcm/send"

 
        payload = json.dumps( {
              # "to": "",
               "to":"dUzGdt5-QXqwda56ASjOJg:APA91bEwBfwRJoIEXPffZ0JBytbvTc6UGdcLSuNE04rrsaOFpqqaPofYlHAswxqJn2pDLPUT4Y5F-fm35GnMl5Ph7cCF-g6_Fhj_Qc-CfMW4F1k_nYC6hgVy3o_tCPe0XbPpYXK2u6UL",
              "notification": {
                "body": message,
                "title": title
              }
            })
        response = requests.request("POST", reqUrl, data=payload,  headers=headersList)
        print(response.content)