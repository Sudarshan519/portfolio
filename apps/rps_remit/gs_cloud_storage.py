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


def download_blob( blob_name):
    storage_client = storage.Client()

    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)
    return blob
    # blob.download_to_filename(destination_path)

    print(f"Image {blob_name} downloaded to {destination_path}")

# download_blob(bucket_name, blob_name, destination_path)

def generate_signed_url( blob_name):
    storage_client = storage.Client()
    print(blob_name)
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)

    expiration = 3600  # URL expiration time in seconds (1 hour)
    signed_url = blob.generate_signed_url(
        version='v4',
        expiration=expiration,
        method='GET'
    )

    return signed_url


def get_public_url(bucket_name, blob_name):
    storage_client = storage.Client()
    # Assuming you have already authenticated using storage.Client()
    blob = storage_client.bucket(bucket_name).blob(blob_name)
    public_url = blob.public_url

    return public_url

# public_download_url = get_public_url(bucket_name, blob_name)
# print(f"Public Download URL: {public_download_url}"