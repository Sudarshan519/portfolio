from google.cloud import storage
import os
# app = FastAPI()

# Set the path to your service account key JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "rasanadmin-72aed785bfb5.json"

# Replace with your actual Google Cloud Storage bucket name
BUCKET_NAME = "rasanadmin.appspot.com"

def upload_to_gcs(blob_name, file_content,content_type):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)
    # Set the proper content type for the image (e.g., "image/jpeg", "image/png", etc.)
    # content_type = file_content.content_type  # Change this based on your image type

    blob.upload_from_string(file_content,content_type)

# @app.post("/upload/")
async def upload_file(file):
    file_content = await file.read()
    upload_to_gcs(file.filename, file_content)
    return {"message": "File uploaded successfully"}

