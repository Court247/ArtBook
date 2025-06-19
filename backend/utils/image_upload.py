import firebase_admin
from firebase_admin import storage
from uuid import uuid4

# Initialize in firebase_auth.py — just make sure it's called before this
bucket = storage.bucket()

def upload_image_file(file, folder="posts"):
    """
    Uploads a file-like object to Firebase Storage and returns its public URL.
    """
    unique_filename = f"{folder}/{uuid4()}"
    blob = bucket.blob(unique_filename)
    blob.upload_from_file(file)
    blob.make_public()
    return blob.public_url
