import requests
import json

reqUrl = "https://fcm.googleapis.com/fcm/send"

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)",
 "Authorization": "Bearer ",
 "Content-Type": "application/json" 
}

payload = json.dumps( {
      "to": "",
      "notification": {
        "body": "Urgent!!! $userName requires",
        "title": "Blood Required"
      }
    })

response = requests.request("POST", reqUrl, data=payload,  headers=headersList)

print(response.text)