import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

class Settings:
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    GDB_PATH: str = os.getenv('PROD_GDB' if ENVIRONMENT == 'production' else 'DEV_GDB', '')

settings = Settings()