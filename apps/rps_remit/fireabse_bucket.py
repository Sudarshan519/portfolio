import json

from fastapi import HTTPException, UploadFile
import requests


# def read_config():
#     with open("google-services.json") as config_file:
#         return json.load(config_file)

# config = read_config()
FIREBASE_STORAGE_BUCKET = "gs://rasanadmin.appspot.com"#config["FIREBASE_STORAGE_BUCKET"]
FIREBASE_API_KEY = "AIzaSyAeEZJKo7GIUtyOQKF1mS40ePL-TxUG3ZI"#config["FIREBASE_API_KEY"]

# @app.post("/upload/")
async def upload_file(file):
    url = f"{FIREBASE_STORAGE_BUCKET}/{file.filename}"
    headers = {
        "Authorization": f"Bearer {FIREBASE_API_KEY}",
        "Content-Type": "application/octet-stream"
    }
    response = requests.put(url, headers=headers, data=await file.read())
    if response.status_code == 200:
        print(FIREBASE_STORAGE_BUCKET+file.filename)
        return {"message": "File uploaded successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

# @app.get("/download/{filename}")
async def download_file(filename: str):
    url = f"{FIREBASE_STORAGE_BUCKET}/{filename}"
    headers = {
        "Authorization": f"Bearer {FIREBASE_API_KEY}",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)