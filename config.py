# config.py
import os
from dotenv import load_dotenv

# Load .env and overwrite anything already set in the OS
load_dotenv(override=True)

class Settings:
    # bytes-encoded secret for HMAC
    GITHUB_SECRET = os.environ.get("GITHUB_SECRET", "").encode()

    # Mongo
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    DB_NAME   = os.environ.get("DB_NAME", "webhook_db")
    COLL_NAME = os.environ.get("COLL_NAME", "events")

settings = Settings()
