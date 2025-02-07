import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "123456")
    SESSION_TYPE = "filesystem"
    UPLOAD_FOLDER = "uploads"
    
    # Ensure the uploads folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    # Hyperbolic API Configuration
    API_URL = "https://api.hyperbolic.xyz/v1/chat/completions"
    API_HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyYWNoZWFsLmxlZUBmbGV4aW5mcmEuY29tLm15IiwiaWF0IjoxNzM4ODEyMDgzfQ.8jhzzRy0MnQmucU2a1KM3wr1eaO5Nng0YS5lrSk3K6c"
    }
