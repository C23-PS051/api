import firebase_admin
from firebase_admin import credentials
import os
from dotenv import load_dotenv

load_dotenv()

app = firebase_admin.initialize_app(credentials.Certificate(os.getenv("SERVICE_ACCOUNT_FILE_PATH")))

if __name__ == "__main__":
    print(app)