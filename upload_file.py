import requests
import time

def current_milli_time():
    return round(time.time() * 1000)
def firebase_upload(bytes,ext,filename):
    # print(bytes)
    # print(ext)
    # print(filename)
# """
# Executes a POST request to upload an image to Firebase Storage.
# DEMONSTRATION ONLY, USE NO FURTHER!
# args: None
# returns: response (json) with the response to the request
# usage: res = firebase_upload()
# """
    response = None

    file2upload = "Edge_Sample.png"
    # file_binary = open(file2upload, "rb").read()

    # HTTP
    
    url2file = f'https://firebasestorage.googleapis.com/v0/b/rasanadmin.appspot.com/o/stash%2F{current_milli_time()}{filename}'
    # headers = {"Content-Type": "application/octet-stream"}

    r = requests.post(url2file, data=bytes, )#headers=headers
    response = r.json()
    # https://firebasestorage.googleapis.com/v0/b/rasanadmin.appspot.com/o/stash%2Fyour_pic.png?alt=media&token=8a561e26-1325-419c-af09-e95d7112dcf5
    name=response['name']
    list=name.split('/')
    url=f"https://firebasestorage.googleapis.com/v0/b/rasanadmin.appspot.com/o/stash%2F{list[1]}?alt=media&token={response['downloadTokens']}"
    # print(url)
    # f = open("uploaded.txt", "a")
    # f.write(url)
    # f.close()
    return url

# resp=firebase_upload()
# print("https://firebasestorage.googleapis.com/v0/b/rasanadmin.appspot.com/"+resp['name'])