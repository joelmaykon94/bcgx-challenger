import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_URL = os.getenv("API_URL", "http://localhost:8000")

settings = Settings()
